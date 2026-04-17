# Track Specification - HU27 - Filtrar reportes

## Overview
Esta funcionalidad potencia el mÃ³dulo de reportes para docentes del colegio Pedro Abel Labarthe Durand, permitiÃ©ndole un anÃ¡lisis de datos mÃ¡s preciso. Se implementarÃ¡ un sistema de filtrado avanzado por rangos de fechas y temas especÃ­ficos, optimizando la experiencia mediante actualizaciones asÃ­ncronas (AJAX) que refrescan grÃ¡ficos y tablas instantÃ¡neamente.

## Functional Requirements
- **Filtro por Rango de Fechas:**
  - Selectores de fecha `Inicio` y `Fin` para acotar los resultados del progreso estudiantil.
  - Los promedios del dashboard deben recalcularse dinÃ¡micamente segÃºn el periodo seleccionado.
- **Filtro por Tema EspecÃ­fico:**
  - MenÃº desplegable para seleccionar un tema de geometrÃ­a (Segmentos, Ãngulos, etc.).
  - Al seleccionar un tema, el reporte individual debe resaltar el desempeño solo en ese tema.
- **Interactividad AJAX:**
  - Implementar un mecanismo asÃ­ncrono para que al cambiar un filtro o hacer clic en \"Filtrar\", los componentes del dashboard (Chart.js y tablas) se actualicen sin recargar el navegador.
- **ValidaciÃ³n de Consistencia:**
  - Asegurar que los filtros por Aula (Grado/SecciÃ³n) sigan funcionando en conjunto con los nuevos filtros de fecha y tema.

## Technical Constraints
- Utilizar `fetch` API en JavaScript para las peticiones asÃ­ncronas.
- Crear un endpoint JSON en el backend que devuelva las mÃ©tricas calculadas y los datos de los estudiantes para el frontend.
- Mantener el control de acceso estricto para docentes en el nuevo endpoint.

## Acceptance Criteria
- El docente puede ver el progreso de los estudiantes en un rango de fechas (ej: de marzo a abril).
- Los grÃ¡ficos de Chart.js se actualizan sin recarga visual de la pÃ¡gina al aplicar filtros.
- El filtrado por tema muestra correctamente el dominio individual de los estudiantes en dicho tema.
- La combinaciÃ³n de mÃºltiples filtros (SecciÃ³n + Fecha + Tema) devuelve resultados exactos.

## Out of Scope
- Persistencia de filtros entre sesiones.
- ExportaciÃ³n de la vista filtrada (Cubierto en track de exportaciÃ³n).
