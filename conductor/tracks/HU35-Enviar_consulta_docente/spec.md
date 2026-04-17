# Track Specification - HU35 - Enviar consulta al docente

## 1. Overview
Esta funcionalidad permite a los estudiantes enviar dudas o consultas directamente al docente responsable a través de un formulario de contacto. El sistema procesará estas consultas enviando un correo electrónico detallado a la dirección configurada, permitiendo al docente responder de forma externa.

## 2. Functional Requirements
- **Acceso Global:** Un enlace "Contactar Docente" estará disponible en la barra de navegación (Navbar) para ser accesible desde cualquier parte del sistema.
- **Formulario de Consulta:**
    - Campos requeridos: Asunto y Mensaje.
    - Campos automáticos (si el usuario está autenticado): Nombre completo y correo del estudiante.
    - Contexto Opcional: El formulario debe capturar automáticamente si el estudiante está consultando desde un tema o ejercicio específico (mediante parámetros en la URL o campos ocultos).
- **Procesamiento:**
    - El sistema NO almacenará los mensajes en la base de datos (por solicitud del usuario).
    - El sistema enviará un correo electrónico a `luisugaz63@gmail.com`.
    - El correo incluirá: Datos del estudiante, Asunto, Mensaje y el contexto (Tema/Ejercicio) si está disponible.
- **Feedback al Estudiante:** Mostrar un mensaje de éxito ("Consulta enviada correctamente") tras el envío exitoso.

## 3. Non-Functional Requirements
- **Idioma:** Toda la interfaz y los correos generados deben estar en español.
- **Seguridad:** El formulario debe estar protegido contra envíos masivos (CSRF y validación de sesión).
- **Configuración:** La dirección de correo de destino y los parámetros SMTP deben estar configurados en `settings.py`.

## 4. Acceptance Criteria
- **Escenario: Envío de consulta general**
    - **Dado** que el estudiante autenticado hace clic en "Contactar Docente" en la Navbar.
    - **Cuando** completa el asunto y el mensaje y presiona "Enviar".
    - **Entonces** el sistema envía un correo a `luisugaz63@gmail.com` y muestra un mensaje de éxito.
- **Escenario: Envío con contexto de ejercicio**
    - **Dado** que el estudiante está resolviendo un ejercicio específico.
    - **Cuando** abre el formulario de contacto.
    - **Entonces** el formulario incluye automáticamente la información del ejercicio actual.
- **Escenario: Validación de campos**
    - **Dado** que el estudiante deja campos vacíos.
    - **Cuando** intenta enviar el formulario.
    - **Entonces** el sistema impide el envío y muestra errores de validación en español.

## 5. Out of Scope
- Almacenamiento de consultas en la base de datos.
- Chat en tiempo real.
- Panel de gestión de mensajes dentro del sistema para el docente.
- Respuesta del docente a través de la plataforma.
