# Implementation Plan - HU27 - Filtrar reportes

Este plan detalla los pasos para evolucionar el dashboard docente hacia una interfaz interactiva y asÃ­ncrona basada en filtros avanzados.

## Fase 1: Endpoint de Datos (Backend)
- [x] **Tarea: Crear Vista de API para Reportes (JSON)**
    - [x] Implementar una vista `ReportesDataJSONView` que acepte parÃ¡metros GET (fecha_inicio, fecha_fin, tema, grado, seccion).
    - [x] Reutilizar `get_classroom_performance_summary` integrando los nuevos filtros de fecha y tema.
    - [x] Retornar un objeto JSON con el resumen, los datos para Chart.js y la lista de estudiantes.
- [x] **Tarea: Conductor - User Manual Verification 'Fase 1: API de Datos' (Protocol in workflow.md)**

## Fase 2: Interactividad AsÃ­ncrona (Frontend)
- [x] **Tarea: Refactorizar Dashboard para Carga AJAX**
    - [x] Modularizar la creaciÃ³n de grÃ¡ficos en una funciÃ³n JavaScript reutilizable.
    - [x] Implementar lÃ³gica de `fetch` para llamar al nuevo endpoint al enviar el formulario de filtros.
    - [x] Actualizar dinÃ¡micamente las tarjetas de resumen y la tabla de estudiantes mediante JavaScript.
- [x] **Tarea: Implementar Selectores de Fecha y Tema**
    - [x] AÃ±adir inputs de tipo `date` y un select de `tema` al formulario de filtros en `reportes_docente.html`.
- [x] **Tarea: Conductor - User Manual Verification 'Fase 2: Frontend AJAX' (Protocol in workflow.md)**

## Fase 3: ValidaciÃ³n y Cobertura
- [x] **Tarea: Pruebas de IntegraciÃ³n de Filtros (TDD)**
    - [x] Escribir pruebas para validar que la combinaciÃ³n de filtros devuelva los datos correctos en el JSON.
- [x] **Tarea: VerificaciÃ³n Final y Cobertura**
    - [x] Ejecutar todas las pruebas del track y asegurar >80% de cobertura en la lÃ³gica de filtrado.
- [x] **Tarea: Conductor - User Manual Verification 'Fase 3: ValidaciÃ³n Final' (Protocol in workflow.md)**
