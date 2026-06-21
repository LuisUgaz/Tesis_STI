from __future__ import annotations

import csv
import html
import logging
import os
import random
import re
from collections import deque
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup
from locust import HttpUser, between, task
from locust.exception import StopUser

logger = logging.getLogger(__name__)


# ============================================================
# CREDENCIALES OPCIONALES DESDE CSV
# ============================================================

# Formato esperado del CSV:
# username,password
# estudiante_test_001,Password123*
# estudiante_test_002,Password123*
#
# Para usarlo:
#   PowerShell:
#   $env:LOCUST_CREDENTIALS_FILE="credenciales_locust.csv"
#
# Si no se configura el CSV, se utilizan LOCUST_USERNAME y
# LOCUST_PASSWORD para todos los usuarios virtuales.
_CREDENTIALS_FILE = os.getenv("LOCUST_CREDENTIALS_FILE", "").strip()
_CREDENTIALS_POOL: deque[tuple[str, str]] = deque()


def _cargar_credenciales() -> None:
    if not _CREDENTIALS_FILE:
        return

    ruta = Path(_CREDENTIALS_FILE)

    if not ruta.exists():
        raise RuntimeError(
            f"No existe el archivo de credenciales: {ruta}"
        )

    with ruta.open("r", encoding="utf-8-sig", newline="") as archivo:
        lector = csv.DictReader(archivo)

        campos = set(lector.fieldnames or [])
        if not {"username", "password"}.issubset(campos):
            raise RuntimeError(
                "El CSV de credenciales debe contener las columnas "
                "'username' y 'password'."
            )

        for fila in lector:
            username = (fila.get("username") or "").strip()
            password = (fila.get("password") or "").strip()

            if username and password:
                _CREDENTIALS_POOL.append((username, password))

    if not _CREDENTIALS_POOL:
        raise RuntimeError(
            "El archivo de credenciales no contiene cuentas válidas."
        )


_cargar_credenciales()


class EstudianteSTI(HttpUser):
    """
    Usuario virtual que representa a un estudiante autenticado.

    Flujo:
    1. Abre el formulario de inicio de sesión.
    2. Obtiene el token CSRF.
    3. Envía las credenciales.
    4. Verifica que la sesión sea válida.
    5. Descubre rutas reales desde enlaces HTML.
    6. Ejecuta tareas solamente si el usuario está autenticado.
    """

    host = os.getenv(
        "LOCUST_HOST",
        "http://127.0.0.1:8000",
    )

    wait_time = between(1, 3)

    LOGIN_URL = os.getenv(
        "LOCUST_LOGIN_URL",
        "/auth/login/",
    )

    TEMAS_URL = os.getenv(
        "LOCUST_TEMAS_URL",
        "/tutoria/temas/",
    )

    PROGRESO_URL = os.getenv(
        "LOCUST_PROGRESO_URL",
        "/auth/mi-progreso/",
    )

    HISTORIAL_URL = os.getenv(
        "LOCUST_HISTORIAL_URL",
        "/evaluar/historial/",
    )

    CONTACTO_URL = os.getenv(
        "LOCUST_CONTACTO_URL",
        "/auth/contacto/",
    )

    VALIDAR_PRACTICA_URL = os.getenv(
        "LOCUST_VALIDAR_PRACTICA_URL",
        "/evaluar/practica/validar/",
    )

    REQUEST_TIMEOUT = float(
        os.getenv("LOCUST_REQUEST_TIMEOUT", "20")
    )

    # Solo admite letras, números, guion y guion bajo.
    TEMA_PATTERN = re.compile(
        r"^/tutoria/temas/(?P<slug>[A-Za-z0-9_-]+)/?$"
    )

    DIAGNOSTICO_PATTERN = re.compile(
        r"^/evaluar/diagnostico/rendir/(?P<id>\d+)/?$"
    )

    RESULTADOS_PATTERN = re.compile(
        r"^/evaluar/(?:diagnostico/)?resultados(?:/\d+)?/?$"
    )

    def on_start(self) -> None:
        self.autenticado = False
        self.tema_slugs: list[str] = []
        self.diagnostico_url: Optional[str] = None
        self.resultados_url: Optional[str] = None
        self._credencial_del_pool = False

        self.username, self.password = self.obtener_credenciales()

        diagnostico_configurado = os.getenv(
            "LOCUST_DIAGNOSTICO_URL",
            "",
        ).strip()

        resultados_configurados = os.getenv(
            "LOCUST_RESULTADOS_URL",
            "",
        ).strip()

        if diagnostico_configurado:
            self.diagnostico_url = self.normalizar_ruta(
                diagnostico_configurado
            )

        if resultados_configurados:
            self.resultados_url = self.normalizar_ruta(
                resultados_configurados
            )

        if not self.iniciar_sesion():
            raise StopUser()

        self.autenticado = True
        self.descubrir_navegacion()

    def on_stop(self) -> None:
        """
        Devuelve la credencial al pool cuando el usuario termina.
        """
        if (
            self._credencial_del_pool
            and self.username
            and self.password
        ):
            _CREDENTIALS_POOL.append(
                (self.username, self.password)
            )

    # ========================================================
    # CREDENCIALES
    # ========================================================

    def obtener_credenciales(self) -> tuple[str, str]:
        if _CREDENTIALS_FILE:
            try:
                username, password = _CREDENTIALS_POOL.popleft()
            except IndexError:
                logger.error(
                    "No quedan credenciales disponibles en el CSV."
                )
                raise StopUser()

            self._credencial_del_pool = True
            return username, password

        username = os.getenv(
            "LOCUST_USERNAME",
            "estudiante_test",
        ).strip()

        password = os.getenv(
            "LOCUST_PASSWORD",
            "Password123*",
        ).strip()

        if not username or not password:
            raise RuntimeError(
                "Debes definir LOCUST_USERNAME y LOCUST_PASSWORD "
                "o configurar LOCUST_CREDENTIALS_FILE."
            )

        return username, password

    # ========================================================
    # AUTENTICACIÓN
    # ========================================================

    def iniciar_sesion(self) -> bool:
        csrf_token: Optional[str] = None

        with self.client.get(
            self.LOGIN_URL,
            name="01 - Abrir inicio de sesión",
            catch_response=True,
            allow_redirects=True,
            timeout=self.REQUEST_TIMEOUT,
        ) as login_page:
            error_red = getattr(login_page, "error", None)

            if error_red:
                login_page.failure(
                    f"Error de red al abrir el login: {error_red}"
                )
                return False

            if login_page.status_code != 200:
                login_page.failure(
                    "No se pudo abrir el login. "
                    f"HTTP {login_page.status_code}."
                )
                return False

            if not self.es_url_login(login_page.url):
                login_page.failure(
                    "La URL configurada no terminó en el login. "
                    f"URL final: {login_page.url}"
                )
                return False

            csrf_token = self.extraer_csrf(login_page.text)

            if not csrf_token:
                csrf_token = (
                    login_page.cookies.get("csrftoken")
                    or self.client.cookies.get("csrftoken")
                )

            if not csrf_token:
                login_page.failure(
                    "No se encontró el token CSRF en el formulario "
                    "ni en las cookies."
                )
                return False

            login_page.success()

        with self.client.post(
            self.LOGIN_URL,
            data={
                "username": self.username,
                "password": self.password,
                "csrfmiddlewaretoken": csrf_token,
                "remember_me": "on",
            },
            headers={
                "Referer": urljoin(
                    self.host,
                    self.LOGIN_URL,
                ),
                "X-CSRFToken": csrf_token,
            },
            name="02 - Autenticar estudiante",
            catch_response=True,
            allow_redirects=False,
            timeout=self.REQUEST_TIMEOUT,
        ) as response:
            error_red = getattr(response, "error", None)

            if error_red:
                response.failure(
                    f"Error de red durante el login: {error_red}"
                )
                return False

            if response.status_code == 403:
                response.failure(
                    "El login devolvió HTTP 403. "
                    "Revisar CSRF, Referer y configuración de Django."
                )
                return False

            if response.status_code >= 500:
                response.failure(
                    "El servidor produjo un error interno durante "
                    f"la autenticación. HTTP {response.status_code}."
                )
                return False

            if response.status_code in (301, 302, 303, 307, 308):
                destino = response.headers.get("Location", "").strip()

                if not destino:
                    response.failure(
                        "El login redirigió sin cabecera Location."
                    )
                    return False

                destino_normalizado = self.normalizar_ruta(destino)

                if not destino_normalizado:
                    response.failure(
                        "La redirección del login contiene una URL inválida."
                    )
                    return False

                if self.es_url_login(
                    urljoin(self.host, destino_normalizado)
                ):
                    response.failure(
                        "El sistema redirigió nuevamente al login."
                    )
                    return False

                # El POST fue válido. La verificación se registra
                # en una solicitud separada para evitar doble conteo.
                response.success()

                return self.verificar_sesion(destino_normalizado)

            if response.status_code == 200:
                # Algunos proyectos renderizan directamente la página
                # de destino sin devolver 302.
                if self.contiene_formulario_login(response.text):
                    response.failure(
                        "El login devolvió HTTP 200 y mostró nuevamente "
                        "el formulario. Verifica las credenciales."
                    )
                    return False

                if not self.client.cookies.get("sessionid"):
                    response.failure(
                        "El login devolvió HTTP 200, pero no se encontró "
                        "una cookie de sesión."
                    )
                    return False

                response.success()
                self.procesar_enlaces(response.text)
                return True

            response.failure(
                "Respuesta inesperada durante el login: "
                f"HTTP {response.status_code}."
            )
            return False

    def verificar_sesion(self, destino: str) -> bool:
        with self.client.get(
            destino,
            name="02.1 - Verificar sesión autenticada",
            catch_response=True,
            allow_redirects=True,
            timeout=self.REQUEST_TIMEOUT,
        ) as verificacion:
            error_red = getattr(verificacion, "error", None)

            if error_red:
                verificacion.failure(
                    "Error de red al verificar la sesión: "
                    f"{error_red}"
                )
                return False

            if verificacion.status_code != 200:
                verificacion.failure(
                    "No se pudo verificar la sesión. "
                    f"HTTP {verificacion.status_code}."
                )
                return False

            if self.es_url_login(verificacion.url):
                verificacion.failure(
                    "La verificación terminó nuevamente en el login."
                )
                return False

            if self.contiene_formulario_login(verificacion.text):
                verificacion.failure(
                    "La página final contiene nuevamente el formulario "
                    "de inicio de sesión."
                )
                return False

            if not self.client.cookies.get("sessionid"):
                verificacion.failure(
                    "La respuesta fue correcta, pero no existe "
                    "una cookie de sesión."
                )
                return False

            self.procesar_enlaces(verificacion.text)
            verificacion.success()
            return True

    def extraer_csrf(self, contenido_html: str) -> Optional[str]:
        soup = BeautifulSoup(contenido_html, "html.parser")

        csrf_input = soup.select_one(
            'input[name="csrfmiddlewaretoken"]'
        )

        if not csrf_input:
            return None

        valor = csrf_input.get("value")

        if not valor:
            return None

        return str(valor).strip()

    def es_url_login(self, url: str) -> bool:
        ruta_actual = urlparse(url).path.rstrip("/")
        ruta_login = urlparse(self.LOGIN_URL).path.rstrip("/")
        return ruta_actual == ruta_login

    def contiene_formulario_login(
        self,
        contenido_html: str,
    ) -> bool:
        soup = BeautifulSoup(contenido_html, "html.parser")

        password_input = soup.select_one(
            'input[type="password"]'
        )

        usuario_input = soup.select_one(
            'input[name="username"], input[name="email"]'
        )

        return bool(password_input and usuario_input)

    # ========================================================
    # VALIDACIÓN Y DESCUBRIMIENTO DE ENLACES
    # ========================================================

    def normalizar_ruta(self, href: str) -> Optional[str]:
        if not href:
            return None

        href = html.unescape(str(href)).strip()

        if not href:
            return None

        if href.lower().startswith(
            ("javascript:", "mailto:", "tel:")
        ):
            return None

        if any(
            caracter in href
            for caracter in ("<", ">", '"', "'")
        ):
            return None

        url_absoluta = urljoin(f"{self.host}/", href)
        url_parseada = urlparse(url_absoluta)
        host_esperado = urlparse(self.host).netloc

        if url_parseada.netloc != host_esperado:
            return None

        ruta = url_parseada.path or "/"

        if url_parseada.query:
            ruta = f"{ruta}?{url_parseada.query}"

        return ruta

    def procesar_enlaces(self, contenido_html: str) -> None:
        soup = BeautifulSoup(contenido_html, "html.parser")
        slugs_encontrados = set(self.tema_slugs)

        for enlace in soup.select("a[href]"):
            href = enlace.get("href")
            ruta = self.normalizar_ruta(str(href or ""))

            if not ruta:
                continue

            path = urlparse(ruta).path

            tema_match = self.TEMA_PATTERN.fullmatch(path)

            if tema_match:
                slug = tema_match.group("slug")

                if re.fullmatch(r"[A-Za-z0-9_-]+", slug):
                    slugs_encontrados.add(slug)

            diagnostico_match = (
                self.DIAGNOSTICO_PATTERN.fullmatch(path)
            )

            if diagnostico_match and not self.diagnostico_url:
                self.diagnostico_url = ruta

            resultado_match = (
                self.RESULTADOS_PATTERN.fullmatch(path)
            )

            if resultado_match and not self.resultados_url:
                self.resultados_url = ruta

        self.tema_slugs = sorted(slugs_encontrados)

    def descubrir_navegacion(self) -> None:
        paginas = (
            ("/", "03.1 - Descubrir enlaces en inicio"),
            (
                self.TEMAS_URL,
                "03.2 - Descubrir enlaces de temas",
            ),
        )

        for ruta, nombre in paginas:
            with self.client.get(
                ruta,
                name=nombre,
                catch_response=True,
                allow_redirects=True,
                timeout=self.REQUEST_TIMEOUT,
            ) as response:
                error_red = getattr(response, "error", None)

                if error_red:
                    response.failure(
                        f"Error de red al descubrir enlaces: {error_red}"
                    )
                    continue

                if response.status_code != 200:
                    response.failure(
                        "No se pudieron descubrir enlaces. "
                        f"HTTP {response.status_code}."
                    )
                    continue

                if self.es_url_login(response.url):
                    response.failure(
                        "La búsqueda de enlaces redirigió al login."
                    )
                    continue

                self.procesar_enlaces(response.text)
                response.success()

        logger.info(
            "Usuario %s: temas=%s, diagnóstico=%s, resultados=%s",
            self.username,
            self.tema_slugs,
            self.diagnostico_url,
            self.resultados_url,
        )

    # ========================================================
    # PETICIONES COMUNES
    # ========================================================

    def consultar_pagina(
        self,
        ruta: str,
        nombre: str,
    ) -> Optional[str]:
        if not self.autenticado:
            raise StopUser()

        ruta_normalizada = self.normalizar_ruta(ruta)

        if not ruta_normalizada:
            logger.warning(
                "Se descartó una ruta inválida: %r",
                ruta,
            )
            return None

        with self.client.get(
            ruta_normalizada,
            catch_response=True,
            allow_redirects=True,
            timeout=self.REQUEST_TIMEOUT,
            name=nombre,
        ) as response:
            error_red = getattr(response, "error", None)

            if error_red:
                response.failure(
                    "Error de red o tiempo de espera en "
                    f"{ruta_normalizada}: {error_red}"
                )
                return None

            if response.status_code != 200:
                response.failure(
                    "Respuesta inesperada en "
                    f"{ruta_normalizada}: "
                    f"HTTP {response.status_code}."
                )
                return None

            if self.es_url_login(response.url):
                response.failure(
                    "La sesión expiró o la ruta redirigió al login."
                )
                self.autenticado = False
                raise StopUser()

            if self.contiene_formulario_login(response.text):
                response.failure(
                    "La respuesta contiene el formulario de login."
                )
                self.autenticado = False
                raise StopUser()

            self.procesar_enlaces(response.text)
            response.success()
            return response.text

    # ========================================================
    # TAREAS DE LECTURA
    # ========================================================

    @task(5)
    def consultar_inicio(self) -> None:
        self.consultar_pagina(
            "/",
            "GET - Página de inicio",
        )

    @task(4)
    def consultar_temas(self) -> None:
        self.consultar_pagina(
            self.TEMAS_URL,
            "GET - Listado de temas",
        )

    @task(3)
    def consultar_progreso(self) -> None:
        self.consultar_pagina(
            self.PROGRESO_URL,
            "GET - Mi progreso",
        )

    @task(3)
    def consultar_historial(self) -> None:
        self.consultar_pagina(
            self.HISTORIAL_URL,
            "GET - Historial de resultados",
        )

    @task(2)
    def consultar_perfil(self) -> None:
        self.consultar_pagina(
            f"/auth/profile/{self.username}/",
            "GET - Perfil del estudiante",
        )

    @task(3)
    def consultar_detalle_tema(self) -> None:
        if not self.tema_slugs:
            return

        slug = random.choice(self.tema_slugs)

        self.consultar_pagina(
            f"/tutoria/temas/{slug}/",
            "GET - Detalle de tema",
        )

    @task(2)
    def consultar_teoria_tema(self) -> None:
        if not self.tema_slugs:
            return

        slug = random.choice(self.tema_slugs)

        self.consultar_pagina(
            f"/tutoria/temas/{slug}/?seccion=teoria",
            "GET - Teoría de tema",
        )

    @task(2)
    def consultar_videos_tema(self) -> None:
        if not self.tema_slugs:
            return

        slug = random.choice(self.tema_slugs)

        self.consultar_pagina(
            f"/tutoria/temas/{slug}/?seccion=videos",
            "GET - Videos de tema",
        )

    @task(2)
    def consultar_contacto(self) -> None:
        self.consultar_pagina(
            self.CONTACTO_URL,
            "GET - Página de contacto",
        )

    # ========================================================
    # EJERCICIOS DE PRÁCTICA
    # ========================================================

    @task(3)
    def resolver_ejercicio_practica(self) -> None:
        if not self.tema_slugs:
            return

        slug = random.choice(self.tema_slugs)

        ruta_ejercicios = (
            f"/tutoria/temas/{slug}/?seccion=ejercicios"
        )

        contenido_html: Optional[str] = None

        with self.client.get(
            ruta_ejercicios,
            name="04 - Ver ejercicios de tema",
            catch_response=True,
            allow_redirects=True,
            timeout=self.REQUEST_TIMEOUT,
        ) as response:
            error_red = getattr(response, "error", None)

            if error_red:
                response.failure(
                    "Error de red al abrir ejercicios: "
                    f"{error_red}"
                )
                return

            if response.status_code != 200:
                response.failure(
                    "No se pudo abrir la sección de ejercicios. "
                    f"HTTP {response.status_code}."
                )
                return

            if self.es_url_login(response.url):
                response.failure(
                    "La sección de ejercicios redirigió al login."
                )
                self.autenticado = False
                raise StopUser()

            contenido_html = response.text
            response.success()

        if not contenido_html:
            return

        soup = BeautifulSoup(contenido_html, "html.parser")
        ejercicios: dict[str, list[str]] = {}

        for opcion in soup.select(
            'input[name^="ejercicio_"][value]'
        ):
            nombre_input = str(opcion.get("name", ""))
            valor = str(opcion.get("value", ""))

            coincidencia = re.fullmatch(
                r"ejercicio_(\d+)",
                nombre_input,
            )

            if not coincidencia or not valor.isdigit():
                continue

            ejercicio_id = coincidencia.group(1)

            ejercicios.setdefault(
                ejercicio_id,
                [],
            ).append(valor)

        if not ejercicios:
            logger.debug(
                "No se encontraron ejercicios en el tema %s.",
                slug,
            )
            return

        ejercicio_id = random.choice(
            list(ejercicios.keys())
        )

        opcion_id = random.choice(
            ejercicios[ejercicio_id]
        )

        csrf_token = (
            self.client.cookies.get("csrftoken")
            or self.extraer_csrf(contenido_html)
        )

        if not csrf_token:
            logger.warning(
                "No se encontró CSRF para validar el ejercicio %s.",
                ejercicio_id,
            )
            return

        with self.client.post(
            self.VALIDAR_PRACTICA_URL,
            data={
                "ejercicio_id": ejercicio_id,
                "opcion_id": opcion_id,
                "tiempo": random.randint(5, 35),
                "csrfmiddlewaretoken": csrf_token,
            },
            headers={
                "Referer": urljoin(
                    self.host,
                    ruta_ejercicios,
                ),
                "X-CSRFToken": csrf_token,
                "X-Requested-With": "XMLHttpRequest",
            },
            name="05 - Validar respuesta de ejercicio",
            catch_response=True,
            allow_redirects=False,
            timeout=self.REQUEST_TIMEOUT,
        ) as response:
            error_red = getattr(response, "error", None)

            if error_red:
                response.failure(
                    "Error de red al validar el ejercicio: "
                    f"{error_red}"
                )
                return

            if response.status_code == 403:
                response.failure(
                    "La validación devolvió HTTP 403. "
                    "Revisar CSRF y permisos."
                )
                return

            if response.status_code == 404:
                response.failure(
                    "La ruta de validación no existe: "
                    f"{self.VALIDAR_PRACTICA_URL}"
                )
                return

            if response.status_code >= 500:
                response.failure(
                    "Django produjo un error interno al validar "
                    f"el ejercicio. HTTP {response.status_code}."
                )
                return

            if response.status_code not in (200, 201):
                response.failure(
                    "Respuesta inesperada al validar el ejercicio: "
                    f"HTTP {response.status_code}."
                )
                return

            content_type = response.headers.get(
                "Content-Type",
                "",
            ).lower()

            if "application/json" in content_type:
                try:
                    datos = response.json()
                except ValueError:
                    response.failure(
                        "La respuesta declaró ser JSON, pero no "
                        "pudo interpretarse."
                    )
                    return

                if (
                    datos.get("success") is False
                    or datos.get("ok") is False
                ):
                    response.failure(
                        "La API respondió HTTP 200, pero indicó "
                        "que la operación no fue exitosa."
                    )
                    return

            response.success()

    # ========================================================
    # DIAGNÓSTICO Y FEEDBACK
    # ========================================================

    @task(1)
    def consultar_diagnostico(self) -> None:
        if not self.diagnostico_url:
            return

        self.consultar_pagina(
            self.diagnostico_url,
            "GET - Ver examen diagnóstico",
        )

    @task(1)
    def consultar_resultados_diagnostico(self) -> None:
        if not self.resultados_url:
            return

        self.consultar_pagina(
            self.resultados_url,
            "GET - Ver resultados del diagnóstico",
        )

    @task(1)
    def consultar_ia_feedback(self) -> None:
        if not self.resultados_url:
            return

        contenido_html = self.consultar_pagina(
            self.resultados_url,
            "06 - Ver resultados para obtener feedback",
        )

        if not contenido_html:
            return

        respuesta_ids = list(
            set(
                re.findall(
                    r"\bcargarFeedbackIA\s*\(\s*(\d+)\s*\)",
                    contenido_html,
                )
            )
        )

        if not respuesta_ids:
            return

        respuesta_id = random.choice(respuesta_ids)

        self.consultar_pagina(
            f"/evaluar/ia-feedback/{respuesta_id}/",
            "GET - Obtener feedback IA",
        )
