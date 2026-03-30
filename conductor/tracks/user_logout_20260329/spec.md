# Especificación de Pista: Cierre de Sesión de Usuarios (HU03)

## Descripción General
Esta pista implementa la Historia de Usuario HU03: \"Cierre de Sesión\". El objetivo es permitir que los usuarios autenticados (estudiantes y docentes) finalicen su sesión de forma segura, destruyendo los datos de autenticación persistentes en el servidor y redirigiéndolos a la pantalla de acceso.

## Requisitos Funcionales

1.  **Acción de Cierre de Sesión:**
    *   **Invalidación de Sesión:** Uso de la función `logout()` nativa de Django para limpiar la sesión del usuario.
    *   **Seguridad:** Asegurar que las rutas protegidas no sean accesibles mediante el botón \"Atrás\" del navegador después del cierre (manejo de caché/redirección).
2.  **Interfaz de Usuario (UI) y UX:**
    *   **Confirmación Previa:** Implementación de un paso de confirmación (vía JavaScript simple) para validar la intención del usuario antes de ejecutar el cierre.
    *   **Botón de Logout:** Ubicación clara en la barra de navegación o el menú de perfil (coherente con la visual de `HU01` y `HU02`).
3.  **Redirección y Feedback:**
    *   **Destino:** Redirección automática a la **Pantalla de Login**.
    *   **Notificación:** Mostrar un mensaje de éxito informativo (ej. \"Has cerrado sesión exitosamente.\") tras la redirección.

## Requisitos No Funcionales
*   **Modularidad:** Implementación centralizada en `AppGestionUsuario`.
*   **Consistencia:** Alineación con los estándares de seguridad de Django para el manejo de sesiones.

## Criterios de Aceptación

### Escenario: Cierre de sesión exitoso
*   **Dado** que el usuario ha iniciado sesión en el sistema.
*   **Cuando** selecciona la opción \"Cerrar Sesión\" y confirma su decisión.
*   **Entonces** el sistema debe destruir la sesión activa, redirigir al usuario a la pantalla de login y mostrar un mensaje de confirmación.

### Escenario: Verificación de seguridad post-logout
*   **Dado** que un usuario ha cerrado sesión.
*   **Cuando** intenta acceder a una ruta protegida (ej. perfil o panel de control).
*   **Entonces** el sistema debe denegar el acceso y redirigirlo al login.

## Fuera de Alcance
*   Auditoría detallada de tiempos de conexión (logs de sesión).
*   Cierre automático de sesión por inactividad.
*   Cierre de sesión en todos los dispositivos simultáneamente.
