# Specification: HU10 - Acceso a contenido de tema

## Overview
Esta historia de usuario permite a los estudiantes acceder y visualizar el material de aprendizaje (teoría, explicaciones, ejemplos) asociado a un tema específico de geometría. El sistema debe garantizar que el contenido se cargue dinámicamente desde la base de datos y que el acceso esté restringido a estudiantes autenticados y, opcionalmente, a los temas que les han sido recomendados según su desempeño previo.

## Functional Requirements
1. **Navegación por Slug:** Las rutas de acceso a los temas deben ser amigables y limpias, utilizando un campo `slug` (ej: `/tutoria/tema/angulos/`).
2. **Modelo de Contenido Dinámico:** El contenido educativo (HTML enriquecido) se almacenará en un nuevo modelo `ContenidoTema` relacionado con el modelo `Tema`.
3. **Vista de Detalle del Tema:** Al seleccionar un tema, el estudiante será redirigido a una página que muestre el nombre del tema y su contenido educativo asociado.
4. **Control de Acceso (Seguridad):**
   - El acceso está restringido a usuarios con sesión iniciada.
   - El acceso está restringido a usuarios con el rol de 'Estudiante'.
   - Un estudiante solo puede acceder a un tema si este se encuentra en sus recomendaciones vigentes (basado en `RecomendacionEstudiante`).
5. **Validación de Existencia:** Si un estudiante intenta acceder a un tema inexistente o a un tema para el cual no tiene permiso, el sistema debe mostrar un error 404 o redirigir con un mensaje adecuado.

## Non-Functional Requirements
- **Usabilidad:** La interfaz debe ser limpia y legible, facilitando la lectura del contenido teórico.
- **Rendimiento:** La carga del contenido debe ser inmediata (menos de 2 segundos).
- **Seguridad:** Los Slugs deben ser únicos para evitar colisiones de rutas.

## Acceptance Criteria
- **Escenario: Acceso Exitoso**
  - Dado que un estudiante está autenticado y tiene una recomendación para el tema "Ángulos".
  - Cuando accede a `/tutoria/tema/angulos/`.
  - Entonces el sistema muestra el contenido HTML enriquecido almacenado para ese tema.
- **Escenario: Acceso Denegado por Falta de Recomendación**
  - Dado que un estudiante está autenticado pero NO tiene una recomendación para el tema "Triángulos".
  - Cuando intenta acceder a `/tutoria/tema/triangulos/`.
  - Entonces el sistema redirige al estudiante a la lista de temas con un mensaje de advertencia o muestra un error 403/404.
- **Escenario: Acceso Denegado por Falta de Autenticación**
  - Dado que un usuario no ha iniciado sesión.
  - Cuando intenta acceder a cualquier ruta de tema.
  - Entonces el sistema redirige al formulario de inicio de sesión.

## Out of Scope
- Ejercicios interactivos dentro de la vista de teoría (se manejarán en otras HU).
- Videos y evaluaciones detalladas.
- Teoría extensa que requiera paginación (en esta fase).
