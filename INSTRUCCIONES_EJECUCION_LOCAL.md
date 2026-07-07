# Instrucciones para ejecutar el proyecto localmente

Este proyecto es una aplicacion web desarrollada con Django y PostgreSQL. Sigue estos pasos para ejecutarlo en una computadora local.

## 1. Requisitos previos

Instalar previamente:

- Python 3.11 o superior
- PostgreSQL
- Git, opcional si el proyecto se descarga como ZIP

## 2. Abrir la carpeta del proyecto

Ubicate en la raiz del proyecto, donde se encuentra el archivo `manage.py`.

Ejemplo en PowerShell:

```powershell
cd C:\ruta\al\proyecto\Tesis_STI
```

## 3. Colocar el archivo `.env`

El archivo `.env` debe estar en la raiz del proyecto, al mismo nivel que `manage.py`.

Este archivo contiene variables de configuracion como:

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`
- `GEMINI_API_KEY`
- `EMAIL_BACKEND`
- `DOCENTE_EMAIL_DESTINO`

Importante: aunque se entregue el archivo `.env`, la base de datos PostgreSQL debe existir en la computadora local y debe coincidir con los datos configurados en ese archivo.

Por ejemplo, si el `.env` contiene:

```env
DB_NAME=tesis_sti
DB_USER=postgres
DB_PASSWORD=123456
DB_HOST=localhost
DB_PORT=5432
```

Entonces PostgreSQL debe tener una base de datos llamada `tesis_sti`, accesible con el usuario `postgres` y la contrasena indicada.

## 4. Crear la base de datos en PostgreSQL

Abrir PostgreSQL y crear la base de datos indicada en el archivo `.env`.

Ejemplo:

```sql
CREATE DATABASE tesis_sti;
```

Si se usa un usuario distinto, editar el archivo `.env` y ajustar estos valores:

```env
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

Si PostgreSQL requiere permisos adicionales sobre el esquema publico:

```sql
\c tesis_sti
GRANT ALL ON SCHEMA public TO postgres;
```

Reemplaza `postgres` por el usuario configurado en `DB_USER`.

## 5. Crear y activar el entorno virtual

Crear el entorno virtual:

```powershell
python -m venv .venv
```

Activarlo en PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activacion, ejecutar:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 6. Instalar dependencias

Actualizar `pip`:

```powershell
python -m pip install --upgrade pip
```

Instalar las dependencias del proyecto:

```powershell
pip install -r requirements.txt
```

Instalar dependencias adicionales necesarias para este proyecto:

```powershell
pip install psycopg2-binary google-genai pandas
```

Nota: estas dependencias adicionales son necesarias porque el proyecto usa PostgreSQL, el SDK moderno de Gemini y algunos comandos de evaluacion con datos.

## 7. Verificar la configuracion de Django

Ejecutar:

```powershell
python manage.py check
```

Si no aparecen errores, continuar con las migraciones.

## 8. Ejecutar migraciones

```powershell
python manage.py migrate
```

Este comando crea las tablas necesarias en PostgreSQL.

## 9. Crear un usuario administrador

```powershell
python manage.py createsuperuser
```

Completar el nombre de usuario, correo y contrasena solicitados.

## 10. Crear el perfil del administrador

Algunas vistas del sistema esperan que cada usuario tenga un perfil asociado. Despues de crear el superusuario, crear su perfil con:

```powershell
python manage.py shell
```

Dentro del shell de Django, ejecutar:

```python
from django.contrib.auth.models import User
from AppGestionUsuario.models import Profile

u = User.objects.get(username="NOMBRE_DEL_SUPERUSUARIO")
Profile.objects.get_or_create(
    user=u,
    defaults={
        "nombres": "Admin",
        "apellidos": "Local",
        "rol": "Administrador"
    }
)

exit()
```

Reemplazar `NOMBRE_DEL_SUPERUSUARIO` por el usuario creado en el paso anterior.

## 11. Ejecutar el servidor local

```powershell
python manage.py runserver
```

Abrir en el navegador:

```text
http://127.0.0.1:8000/
```

Panel de administracion de Django:

```text
http://127.0.0.1:8000/admin/
```

## 12. Datos iniciales

Las migraciones crean algunas insignias iniciales, pero el proyecto no incluye automaticamente temas, preguntas, examenes, videos o contenido teorico.

Desde el panel de administracion o desde las pantallas del sistema se pueden crear:

- Temas
- Contenido teorico
- Videos o enlaces de YouTube
- Examenes diagnosticos
- Preguntas y opciones
- Ejercicios
- Usuarios con roles `Estudiante`, `Docente` o `Administrador`

## 13. Comandos opcionales

Asignar perfiles de estudiante a usuarios no administradores:

```powershell
python manage.py asignar_estudiantes
```

Generar resultados simulados de diagnostico:

```powershell
python manage.py seed_diagnostico --cantidad 5
```

Generar retroalimentacion con IA para respuestas de diagnostico:

```powershell
python manage.py enriquecer_diagnostico --limit 10
```

Generar metadatos de IA para ejercicios:

```powershell
python manage.py enriquecer_ejercicios --limit 10
```

Evaluar algoritmos de machine learning:

```powershell
python manage.py evaluar_algoritmos
```

Importante: los comandos `enriquecer_diagnostico` y `enriquecer_ejercicios` usan Gemini y requieren que `GEMINI_API_KEY` este configurado en el archivo `.env`.

## 14. Errores frecuentes

### Error: `No module named psycopg2`

Instalar:

```powershell
pip install psycopg2-binary
```

### Error: `No module named google.genai`

Instalar:

```powershell
pip install google-genai
```

### Error de conexion a PostgreSQL

Revisar que:

- PostgreSQL este activo.
- La base de datos exista.
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` y `DB_PORT` coincidan con la configuracion local.

### Error al usar funciones de IA

Revisar que `GEMINI_API_KEY` este configurado en el archivo `.env`.

### Advertencia de Git: `dubious ownership`

Ejecutar:

```powershell
git config --global --add safe.directory "C:/ruta/al/proyecto/Tesis_STI"
```

## 15. Nota sobre archivos multimedia

Las carpetas de archivos subidos, imagenes y videos pueden estar ignoradas por Git, por ejemplo:

- `media/`
- `videos_temas/`
- `videos_thumbnails/`

Si el proyecto depende de PDFs, imagenes o videos locales, estas carpetas deben compartirse aparte junto con el proyecto.

## 16. Nota sobre backup de base de datos

Si se entrega un backup de PostgreSQL junto con el proyecto, el usuario puede restaurarlo para tener datos iniciales como usuarios, temas, preguntas, examenes y contenidos.

Sin backup, el usuario debera crear esos datos manualmente desde el sistema.
