# Track Specification - HU19 - Filtrar historial de resultados

## Overview
Esta historia de usuario extiende la funcionalidad del Historial AcadÃ©mico (HU18), permitiendo a los estudiantes realizar bÃºsquedas precisas de sus actividades pasadas mediante el filtrado por tema y rangos de fechas. El objetivo es facilitar el seguimiento del progreso acadÃ©mico a lo largo del tiempo.

## Functional Requirements
- **Filtro por Rango de Fechas:** El estudiante podrÃ¡ seleccionar una "Fecha de Inicio" y una "Fecha de Fin" para visualizar Ãºnicamente las actividades registradas en ese periodo.
- **Filtro por Tema:** Se mantiene y mejora el filtro por tema de geometrÃ­a ya existente.
- **Filtrado Combinado:** El sistema permitirÃ¡ aplicar simultÃ¡neamente el filtro por Tema y por Rango de Fechas, refinando los resultados de la tabla.
- **Interactividad Visual:** Se implementarÃ¡n selectores de fecha interactivos (Datepicker) para una experiencia de usuario mÃ¡s fluida y moderna.
- **NotificaciÃ³n de Resultados VacÃ­os:** En caso de que no existan registros para los criterios aplicados, el sistema mostrarÃ¡ una notificaciÃ³n clara (Toast/Alerta) informando la ausencia de resultados.
- **Persistencia de Filtros:** Al aplicar los filtros, los valores seleccionados deben permanecer visibles en los campos del formulario tras la recarga de la pÃ¡gina (Server-side rendering).

## Technical Constraints
- El filtrado de datos debe realizarse en el servidor (Django QuerySet) para asegurar el manejo eficiente de grandes volÃºmenes de datos.
- Se debe validar que la "Fecha de Inicio" no sea posterior a la "Fecha de Fin".
- Toda la lÃ³gica debe respetar la privacidad del estudiante (solo sus propios datos).

## Acceptance Criteria
- El estudiante puede seleccionar un rango de fechas y la tabla se actualiza correctamente.
- El estudiante puede combinar el filtro de tema con el rango de fechas.
- Los selectores de fecha son intuitivos y fÃ¡ciles de usar.
- Si no hay resultados, se muestra una notificaciÃ³n de alerta.
- Los registros se muestran en orden cronolÃ³gico descendente por defecto, respetando los filtros.

## Out of Scope
- ExportaciÃ³n de resultados filtrados (PDF/Excel).
- EstadÃ­sticas o grÃ¡ficas comparativas basadas en el filtrado.
- Filtros por puntaje u otras mÃ©tricas cuantitativas avanzadas.
