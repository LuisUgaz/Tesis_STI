# Specification: HU11 - Visualización de marco teórico

## Overview
Esta historia de usuario extiende la vista de detalle de los temas geométricos (HU10) para incluir una estructura de navegación interna mediante un menú lateral (sidebar). El objetivo es permitir al estudiante acceder de forma organizada al "Marco Teórico" del tema seleccionado, manteniendo una página de resumen como punto de entrada inicial y preparando la interfaz para futuras secciones como ejercicios y videos.

## Functional Requirements
1. **Interfaz con Menú Lateral (Sidebar):**
   - La página de detalle del tema (`tema_detalle.html`) debe actualizarse para incluir un menú lateral persistente.
   - El menú debe contener los siguientes enlaces:
     - **Resumen:** Muestra la descripción general del tema.
     - **Marco Teórico:** Muestra el contenido detallado almacenado en `ContenidoTema.cuerpo_html`.
     - **Ejercicios** (Deshabilitado): Marcador de posición para funcionalidad futura.
     - **Videos** (Deshabilitado): Marcador de posición para funcionalidad futura.
2. **Navegación Dinámica (Secciones):**
   - Al entrar en un tema, la sección mostrada por defecto será la "Página de Resumen" utilizando la descripción del modelo `Tema`.
   - Al hacer clic en "Marco Teórico" en el sidebar, el área de contenido principal debe mostrar la teoría detallada de `ContenidoTema`.
3. **Carga de Contenido Real:**
   - Se debe precargar contenido teórico real (HTML enriquecido) para el tema de "Triángulos", incluyendo clasificaciones (según lados y ángulos) y propiedades básicas (suma de ángulos internos).
4. **Validación de Acceso:**
   - Se mantienen las restricciones de acceso de la HU10 (estudiante autenticado y tema recomendado).

## Non-Functional Requirements
- **Consistencia Visual:** El menú lateral debe seguir la línea gráfica gamificada del proyecto.
- **Interactividad:** El cambio entre secciones debe ser fluido (usando parámetros de consulta o rutas simples).

## Acceptance Criteria
- **Escenario: Visualización de Resumen (Default)**
  - Dado que un estudiante está autenticado y accede a un tema recomendado (ej: Triángulos).
  - Cuando se carga la página de detalle.
  - Entonces el sistema muestra la descripción general del tema ("Página de Resumen").
- **Escenario: Cambio a Marco Teórico**
  - Dado que el estudiante se encuentra en la vista de detalle de un tema.
  - Cuando selecciona "Marco Teórico" en el menú lateral.
  - Entonces el sistema muestra el material teórico detallado (HTML) asociado a ese tema.
- **Escenario: Marcadores Futuros**
  - El estudiante debe visualizar las opciones "Ejercicios" y "Videos" en el sidebar, pero estas deben estar claramente indicadas como no disponibles o ser inaccesibles en esta etapa.

## Out of Scope
- Seguimiento de progreso de lectura de la teoría.
- Implementación de la lógica de ejercicios o reproducción de videos.
- Gamificación específica por leer la teoría (puntos/insignias).
- Teoría detallada para temas que no sean "Triángulos" (estos usarán placeholders).
