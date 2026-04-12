# Track Specification - HU20 - Calcular mÃ©tricas acadÃ©micas

## Overview
Esta funcionalidad automatiza el cÃ¡lculo y almacenamiento de mÃ©tricas de desempeÃ±o para cada estudiante dentro del Sistema Tutor Inteligente. El objetivo es proporcionar datos precisos sobre el progreso acadÃ©mico, facilitando la adaptabilidad del sistema y la futura visualizaciÃ³n de resultados para estudiantes y docentes.

## Functional Requirements
- **Modelo de MÃ©tricas:** CreaciÃ³n del modelo `MetricasEstudiante` para persistir:
  - `precision_general`: Porcentaje acumulado de aciertos.
  - `rendimiento_academico`: Promedio de puntajes obtenidos.
  - `tiempo_respuesta_promedio`: Tiempo medio de resoluciÃ³n en segundos.
  - `dominio_por_tema`: Almacenamiento (JSON o Relacional) del nivel de acierto por categorÃ­a de geometrÃ­a.
- **Servicio de CÃ¡lculo AcadÃ©mico:** ImplementaciÃ³n de un mÃ³dulo de servicio (`AppEvaluar/services.py` o similar) con lÃ³gica explÃ­cita para:
  - `actualizar_metricas_estudiante(usuario, actividad_reciente)`: FunciÃ³n principal disparada tras cada evento relevante.
- **ActualizaciÃ³n Incremental:** El cÃ¡lculo optimizarÃ¡ recursos actualizando solo los valores impactados por la Ãºltima actividad registrada (ej. solo el promedio del tema especÃ­fico y el global).
- **Trazabilidad:** La ejecuciÃ³n del servicio serÃ¡ explÃ­cita en las vistas de resultados de ejercicios y exÃ¡menes, permitiendo una depuraciÃ³n clara del flujo de datos.

## Technical Constraints
- Utilizar el modelo `ProgresoEstudiante` y los resultados histÃ³ricos (`ResultadoEjercicio`, `ResultadoDiagnostico`) como base para los cÃ¡lculos.
- El campo `dominio_por_tema` debe ser escalable para nuevos temas aÃ±adidos al sistema.
- Se debe asegurar la integridad de los datos en caso de fallos durante el recÃ¡lculo (transacciones atÃ³micas si es necesario).

## Acceptance Criteria
- Se crea el modelo `MetricasEstudiante` con los campos definidos.
- Las mÃ©tricas se recalculan correctamente al finalizar un examen diagnÃ³stico.
- Las mÃ©tricas se recalculan correctamente tras resolver una sesiÃ³n de prÃ¡ctica.
- El cÃ¡lculo de precisiÃ³n refleja exactamente la relaciÃ³n aciertos/intentos.
- No se utiliza lÃ³gica oculta (Signals) para los cÃ¡lculos principales.

## Out of Scope
- Interfaz grÃ¡fica para visualizar estas mÃ©tricas (Dashboard).
- Reportes comparativos entre diferentes estudiantes.
- ExportaciÃ³n de mÃ©tricas a formatos externos.
