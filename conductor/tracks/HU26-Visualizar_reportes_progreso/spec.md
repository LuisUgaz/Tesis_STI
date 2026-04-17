# Track Specification - HU26 - Visualizar reportes de progreso

## Overview
Esta funcionalidad introduce un mÃ³dulo analÃ­tico exclusivo para docentes y administradores, permitiÃ©ndoles monitorear el avance acadÃ©mico del colegio Pedro Abel Labarthe Durand. El panel proporcionarÃ¡ una visiÃ³n tanto agregada (por aula) como detallada (por estudiante), utilizando una combinaciÃ³n de tablas informativas y grÃ¡ficos interactivos para identificar fortalezas y vacÃ­os de aprendizaje en geometrÃ­a.

## Functional Requirements
- **MÃ³dulo de Reportes Docente:**
  - Acceso restringido mediante decoradores de Django (`@teacher_required` o similar).
  - Dashboard principal con acceso desde el menÃº independiente.
- **Reporte Agregado (Vista de Aula):**
  - EstadÃ­sticas generales: PrecisiÃ³n promedio, total de XP acumulado y temas con mayor dificultad.
  - GrÃ¡ficos dinÃ¡micos (Chart.js) para tendencias de rendimiento por secciÃ³n.
- **Reporte Individual (Vigilancia de Alumno):**
  - Lista de estudiantes filtrable por nombre, grado y secciÃ³n.
  - Detalle expandible por alumno que muestre: Nivel actual, XP, insignias ganadas y dominio por tema.
- **Reporte por Temas/Dificultad:**
  - Desglose de aciertos y errores por cada tema de geometrÃ­a (TriÃ¡ngulos, Segmentos, etc.).
- **Sistema de Filtrado Avanzado:**
  - Capacidad de filtrar datos por Periodo AcadÃ©mico (Grado/SecciÃ³n) y Rangos de Fechas para medir el progreso temporal.

## Technical Constraints
- Implementar el control de acceso asegurando que un estudiante no pueda acceder a la URL de reportes.
- Combinar visualizaciones en HTML/CSS puro (barras de progreso nativas) con Chart.js para grÃ¡ficos de radar o barras.
- Optimizar las consultas a la base de datos (QuerySets) para evitar latencia al procesar mÃ©tricas de mÃºltiples estudiantes.

## Acceptance Criteria
- El docente visualiza el listado completo de sus estudiantes al ingresar a reportes.
- Los grÃ¡ficos de Chart.js cargan correctamente con datos reales de la base de datos.
- El filtrado por grado y secciÃ³n actualiza dinÃ¡micamente los promedios del dashboard.
- Solo usuarios con rol 'Docente' o 'Administrador' pueden ver este mÃ³dulo.

## Out of Scope
- ExportaciÃ³n a PDF/Excel (Cubierto en track `reports_export_20260327`).
- EdiciÃ³n de mÃ©tricas o resultados desde el panel de reportes.
- ComunicaciÃ³n directa (Chat) desde el reporte.
