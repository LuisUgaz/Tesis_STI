# Especificación de Pista: Visualización de Perfil por Rol (HU04)

## Descripción General
Esta pista implementa la Historia de Usuario HU04: \"Visualización de perfil por rol\". El objetivo es permitir que los usuarios autenticados consulten sus datos básicos y académicos registrados en el sistema mediante una interfaz gamificada y diferenciada según su rol (Estudiante, Docente o Administrador).

## Requisitos Funcionales

1.  **Vista de Perfil Personalizada:**
    *   **Acceso:** Solo usuarios autenticados pueden ver su propio perfil.
    *   **URL:** `/auth/profile/<username>/`.
    *   **Lógica:** Validación de que el `<username>` solicitado coincide con el usuario en sesión.
2.  **Visualización Diferenciada por Rol:**
    *   **Para Estudiantes:** Mostrar Nombre Completo, Email, Grado/Sección y Rol.
    *   **Para Docentes/Admin:** Mostrar Nombre Completo y Rol (ocultar campos académicos innecesarios).
3.  **Interfaz de Usuario (UI):**
    *   Estilo **Gamificado (Card Style)**: Uso de una \"Ficha de Personaje\" o tarjeta visualmente atractiva con colores vibrantes.
    *   Coherencia con la línea visual de `HU01` y `HU02`.

## Requisitos No Funcionales
*   **Seguridad:** Aplicación del decorador `@login_required` o mixins de autenticación.
*   **Integridad:** Consulta directa al modelo `Profile` vinculado al `User`.
*   **Privacidad:** Un usuario no puede ver el perfil de otro usuario mediante la URL (redirección o error 403).

## Criterios de Aceptación

### Escenario: Acceso al perfil como Estudiante
*   **Dado** que un Estudiante ha iniciado sesión.
*   **Cuando** accede a su URL de perfil.
*   **Entonces** debe ver una tarjeta con sus nombres, apellidos, correo y grado/sección asignado.

### Escenario: Acceso al perfil como Docente
*   **Dado** que un Docente ha iniciado sesión.
*   **Cuando** accede a su perfil.
*   **Entonces** debe ver su información básica y su rol, sin campos de grado o sección.

### Escenario: Restricción de acceso
*   **Dado** que un usuario NO ha iniciado sesión.
*   **Cuando** intenta acceder a la URL de perfil.
*   **Entonces** el sistema debe redirigirlo a la pantalla de login.

## Fuera de Alcance
*   Edición de datos (nombres, grado, etc.).
*   Subida de foto de perfil (avatar).
*   Visualización de estadísticas de gamificación (puntos, logros).
*   Cambio de contraseña.
