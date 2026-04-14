# Implementation Plan - HU35 - Enviar consulta al docente

Este plan detalla la implementación de la funcionalidad de contacto entre estudiante y docente mediante el envío de correos electrónicos.

## Fase 1: Configuración de Entorno
- [x] Task: Configurar parámetros de Email en `Tesis_STI/settings.py`.
    - [x] Añadir `EMAIL_BACKEND` (consola para desarrollo, SMTP para producción).
    - [x] Añadir `DOCENTE_EMAIL_DESTINO = 'luisugaz63@gmail.com'`.
- [x] Task: Verificar que el servidor de desarrollo pueda emitir correos (backend de consola).

## Fase 2: Formulario y Backend
- [x] Task: Crear `ContactoForm` en `AppGestionUsuario/forms.py`.
    - [x] Campos: `asunto`, `mensaje`.
    - [x] Campos ocultos/opcionales para contexto: `tema_id`, `ejercicio_id`.
- [x] Task: Crear vista `ContactoView` en `AppGestionUsuario/views.py`.
    - [x] Validar que el usuario esté autenticado.
    - [x] Procesar el formulario y enviar el correo usando `django.core.mail.send_mail`.
    - [x] Incluir detalles del estudiante (nombre, correo) y contexto (Tema/Ejercicio) en el cuerpo del mensaje.
- [x] Task: Configurar URL en `AppGestionUsuario/urls.py` para la vista de contacto.

## Fase 3: Interfaz de Usuario
- [x] Task: Crear la plantilla `AppGestionUsuario/contacto.html`.
    - [x] Extender de `home.html`.
    - [x] Diseñar un formulario amigable con Bootstrap 5.
- [x] Task: Integrar el enlace "Contactar Docente" en la Navbar de `templates/home.html`.
    - [x] Asegurar que el enlace pase los parámetros de contexto si están disponibles en la URL actual (opcional/mejora).

## Fase 4: Pruebas y Validación
- [x] Task: Probar el envío de una consulta general.
- [x] Task: Probar el envío de una consulta con contexto (simulando parámetros).
- [x] Task: Verificar que los errores de validación aparezcan en español.
- [x] Task: Conductor - User Manual Verification 'HU35 - Enviar consulta al docente' (Protocol in workflow.md)
