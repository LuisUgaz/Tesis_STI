# HU43 - Visualizar teoría mediante carrusel de imágenes por tema

## Overview
Esta funcionalidad permitirá a los estudiantes visualizar el contenido teórico de cada tema mediante un carrusel de imágenes interactivo. El objetivo es proporcionar una alternativa más dinámica y ligera que la descarga de archivos PDF, permitiendo una navegación fluida entre los conceptos geométricos.

## Functional Requirements
- **Visor de Imágenes:** Se implementará un carrusel en la sección de teoría del detalle del tema.
- **Navegación:** Botones de "Anterior" y "Siguiente" para recorrer las imágenes según su orden.
- **Indicador de Progreso Visual:** Mostrará el formato "Página X de Y".
- **Indicador de Progreso Académico (Incremental):**
  - El sistema calculará el progreso como: `(página_máxima_alcanzada / total_imágenes) * 100`.
  - Este progreso se actualizará cada vez que el estudiante avance a una nueva imagen en el carrusel.
  - La actividad de "Teoría" solo se marcará como **completada** cuando el estudiante llegue a la última imagen.
- **Modo Pantalla Completa:** Implementación de un visor tipo "Lightbox" que amplíe la imagen sobre un fondo oscurecido.
- **Interactividad Avanzada:**
  - **Soporte de Teclado:** Uso de flechas de dirección (izquierda/derecha) para navegar.
  - **Zoom Interactivo:** Funcionalidad para acercar/alejar detalles de la imagen.
- **Gestión de Contenido:** Los docentes podrán subir múltiples imágenes vinculadas a un tema y definir su orden desde el administrador.
- **Compatibilidad con PDF:** El botón de descarga del PDF original se mantendrá como recurso complementario.
- **Estado de Vacío:** Si un tema no tiene imágenes registradas, se mostrará un mensaje descriptivo ("No hay contenido visual disponible para este tema") sin afectar la estabilidad del sistema.

## Non-Functional Requirements
- **Rendimiento:** El carrusel debe ser ligero y fluido, cargando las imágenes bajo demanda si es posible.
- **Tecnología:** Implementado estrictamente con Vanilla JavaScript y CSS (sin librerías externas pesadas).
- **Responsividad:** El carrusel debe adaptarse correctamente a dispositivos móviles y tablets.

## Acceptance Criteria
1. **Visualización:** Al entrar a la sección de teoría de un tema con imágenes, se debe mostrar la primera imagen automáticamente.
2. **Navegación:** Al hacer clic en "Siguiente", se muestra la imagen siguiente y se actualiza el indicador "Página X de Y".
3. **Progreso:** Al avanzar en el carrusel, se debe registrar el porcentaje de avance en el perfil del estudiante.
4. **Pantalla Completa:** Al hacer clic en la imagen, esta debe abrirse en un Lightbox. Al cerrarlo, el estudiante debe volver a la misma imagen del carrusel.
5. **Teclado:** Las flechas del teclado deben permitir navegar entre imágenes.
6. **Sin Imágenes:** Si el tema no tiene imágenes, debe aparecer el mensaje "No hay contenido visual disponible para este tema".

## Out of Scope
- Conversión automática de PDF a imágenes.
- Edición de imágenes desde la plataforma.
- Seguimiento analítico detallado por cada segundo de visualización.
