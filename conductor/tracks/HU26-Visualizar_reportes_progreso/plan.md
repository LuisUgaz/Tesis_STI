# Implementation Plan - HU26 - Visualizar reportes de progreso

Este plan detalla los pasos para construir el sistema de monitoreo docente, asegurando la seguridad de los datos y una visualizaciÃ³n clara del avance estudiantil.

## Fase 1: Estructura y Control de Acceso
- [x] **Tarea: Crear MÃ³dulo de Reportes (AppEvaluar)**
    - [x] Registrar la ruta `/evaluar/reportes/` en `urls.py`.
    - [x] Implementar la vista base `ReportesDocenteView` con el mixin de acceso para docentes.
    - [x] Crear el template base `reportes_docente.html`.
- [ ] **Tarea: Conductor - User Manual Verification 'Fase 1: Estructura y Acceso' (Protocol in workflow.md)**

## Fase 2: Motor de AgregaciÃ³n de Datos (TDD)
- [x] **Tarea: Implementar Servicio de EstadÃ­sticas de Aula (TDD)**
    - [x] Escribir pruebas para el cÃ¡lculo de promedios por grado/secciÃ³n.
    - [x] Implementar en `services_metrics.py` funciones para agrupar desempeÃ±o por tema a nivel de aula.
- [x] **Tarea: Integrar Datos para GrÃ¡ficos**
    - [x] Preparar el JSON de datos necesario para alimentar Chart.js en el frontend.
- [ ] **Tarea: Conductor - User Manual Verification 'Fase 2: AgregaciÃ³n de Datos (TDD)' (Protocol in workflow.md)**

## Fase 3: Interfaz AnalÃ­tica y Filtros
- [x] **Tarea: Implementar Dashboard Principal (UI)**
    - [x] Integrar la librerÃ­a Chart.js vía CDN.
    - [x] Crear tarjetas de resumen (Cards) con HTML/CSS puro para mÃ©tricas rÃ¡pidas.
    - [x] Implementar grÃ¡ficos de barras y radar para comparar temas.
- [x] **Tarea: Listado de Estudiantes y Filtros**
    - [x] Crear tabla de estudiantes con bÃºsqueda por nombre y filtros por secciÃ³n.
    - [x] Implementar lÃ³gica de filtrado asÃ­ncrona o mediante parÃ¡metros GET.
- [x] **Tarea: VerificaciÃ³n Final y Cobertura**
    - [x] Ejecutar todas las pruebas del track y asegurar >80% de cobertura.
- [ ] **Tarea: Conductor - User Manual Verification 'Fase 3: Interfaz AnalÃ­tica' (Protocol in workflow.md)**
