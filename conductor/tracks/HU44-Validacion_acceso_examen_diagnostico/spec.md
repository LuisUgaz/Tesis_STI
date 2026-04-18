# HU44 - Validación de acceso y redirección al examen diagnóstico

## Overview
Esta funcionalidad mejora la experiencia del estudiante al intentar acceder a contenidos restringidos. En lugar de recibir un error de sistema (403), el estudiante será guiado mediante un modal informativo hacia su examen diagnóstico inicial, permitiéndole entender por qué el contenido está bloqueado y cómo desbloquearlo.

## Functional Requirements
- **Redirección Amigable:** La vista `tema_detalle` detectará la falta de recomendación y redirigirá al usuario a la lista de temas usando el framework de mensajes de Django con una etiqueta específica (ej. `info_necesita_examen`).
- **Modal de Bienvenida/Aviso:** En la lista de temas, si se detecta el mensaje correspondiente, se mostrará automáticamente un modal con estilo "Info (Blue)".
- **Interactividad en la Lista:** Si el estudiante intenta hacer clic en un tema bloqueado directamente desde la lista, el sistema disparará el mismo modal en lugar de permitir la navegación.
- **Acceso Directo:** El modal contará con un botón: "Rendir Examen Diagnóstico" que redirigirá a `/evaluar/rendir/1/`.

## Acceptance Criteria (Gherkin)
- **Scenario: Intento de acceso forzado sin recomendación**
  - **Given** que un estudiante no ha realizado el examen diagnóstico.
  - **When** intenta ingresar manualmente a la URL de un tema (ej. `/tutoria/temas/triangulos/`).
  - **Then** el sistema debe redirigirlo a `/tutoria/temas/`.
  - **And** debe mostrar automáticamente un modal informativo.
- **Scenario: Clic en tema bloqueado en la lista**
  - **Given** que el estudiante visualiza la lista de temas pero no tiene recomendaciones.
  - **When** hace clic en el enlace de un tema.
  - **Then** el sistema no debe cambiar de página.
  - **And** debe mostrar el modal de "Examen Requerido".

## Scope
- Modificación de lógica de permisos en `AppTutoria/views.py`.
- Creación de componente Modal en `AppTutoria/templates/AppTutoria/lista_temas.html`.
- Estilos CSS personalizados para el modal (Info Blue).
- Lógica Vanilla JS para interceptar clics y manejar el estado del mensaje.

## Out of Scope
- Seguimiento de cuántas veces se abrió el modal.
- Cambio en el contenido de los exámenes.

## Rules
- **Relación de datos:** Validar contra el modelo `RecomendacionEstudiante`.
- **Tecnología:** Estrictamente Vanilla JavaScript y CSS.
- **Idioma:** Todo en español.
- **Nombres:** Carpeta `HU44-Validacion_acceso_examen_diagnostico`.
- **Git:** No realizar commits.

## Antes de implementar
- Revisar el manejo actual de mensajes en la base de la plantilla.
- Verificar la URL exacta del examen diagnóstico ID 1.
- Identificar los selectores CSS de los enlaces de temas en la lista.
