# Especificación de Pista: Inicio de Sesión de Usuarios (HU02)

## Descripción General
Esta pista implementa la Historia de Usuario HU02: "Inicio de Sesión". El objetivo es permitir que los usuarios registrados (estudiantes y docentes) accedan a su cuenta de forma segura en la plataforma "Sistema Tutor Inteligente Adaptativo para Geometría". Se empleará el sistema de autenticación nativo de Django, manteniendo la coherencia estética con el registro previo (HU01).

## Requisitos Funcionales

1.  **Formulario de Login:**
    *   **Campos Requeridos:** Nombre de Usuario y Contraseña.
    *   **Funcionalidad \"Recordarme\":** Checkbox para habilitar sesiones persistentes (uso de `SESSION_EXPIRE_AT_BROWSER_CLOSE = False`).
2.  **Proceso de Autenticación:**
    *   Validación de credenciales contra la base de datos PostgreSQL mediante `authenticate()` de Django.
    *   Inicio de sesión de usuario mediante `login()`.
3.  **Gestión de Errores:**
    *   Mensaje claro si el nombre de usuario no existe o la contraseña es incorrecta.
    *   Manejo de intentos con campos vacíos.
4.  **Redirección Post-Login:**
    *   Redirección exitosa a una página de inicio general (`Home General (Mock)`).
5.  **Interfaz de Usuario (UI):**
    *   Estilo visual **Gamificado / Juvenil**, consistente con `HU01`.
    *   Uso de mensajes flash para retroalimentación visual (éxito/error).

## Requisitos No Funcionales
*   **Seguridad:** Uso de CSRF tokens en el formulario y almacenamiento seguro de sesiones.
*   **Modularidad:** Implementación dentro de `AppGestionUsuario`.
*   **Consistencia:** Respetar el uso de PostgreSQL y las convenciones de Django.

## Criterios de Aceptación

### Escenario: Inicio de sesión exitoso
*   **Dado** que el usuario está registrado en el sistema.
*   **Cuando** ingresa su nombre de usuario y contraseña correctos.
*   **Entonces** el sistema debe autenticarlo, crear una sesión activa y redirigirlo a la página de inicio.

### Scenario: Credenciales incorrectas
*   **Dado** que el usuario intenta iniciar sesión.
*   **Cuando** ingresa un usuario inexistente o una contraseña inválida.
*   **Entonces** el sistema debe denegar el acceso y mostrar un mensaje de error descriptivo en el formulario.

## Fuera de Alcance
*   Redirección basada en roles específicos (estudiante vs docente).
*   Recuperación de contraseña por correo.
*   Autenticación mediante redes sociales.
*   Bloqueo de cuenta tras múltiples intentos fallidos.
