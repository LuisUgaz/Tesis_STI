# Implementation Plan - HU20 - Calcular mÃ©tricas acadÃ©micas

Este plan detalla los pasos para automatizar el cÃ¡lculo de mÃ©tricas de desempeÃ±o mediante un servicio explÃ­cito y un modelo de datos independiente.

## Fase 1: Modelado e Infraestructura
- [x] **Tarea: Crear el modelo `MetricasEstudiante`** [manual]
    - [ ] Definir el modelo en `AppGestionUsuario/models.py`.
    - [ ] Incluir campos: `precision_general`, `rendimiento_academico`, `tiempo_respuesta_promedio`, `dominio_por_tema` (JSONField).
    - [ ] Generar y aplicar migraciones.
- [x] **Tarea: Estructura del Servicio de MÃ©tricas** [manual]
    - [ ] Crear el archivo `AppEvaluar/services_metrics.py`.
    - [ ] Definir la firma de `actualizar_metricas_estudiante(usuario, actividad_reciente)`.
- [x] **Tarea: Conductor - User Manual Verification 'Fase 1: Modelado e Infraestructura' (Protocol in workflow.md)** [manual]

## Fase 2: LÃ³gica de CÃ¡lculo (TDD)
- [x] **Tarea: Implementar CÃ¡lculo de PrecisiÃ³n y Rendimiento** [manual]
    - [ ] Escribir pruebas unitarias para el cÃ¡lculo incremental de precisiÃ³n.
    - [ ] Implementar la lÃ³gica para actualizar el porcentaje de aciertos global.
- [x] **Tarea: Implementar CÃ¡lculo de Tiempo y Dominio por Tema** [manual]
    - [ ] Escribir pruebas unitarias para el promedio de tiempo y aciertos por categorÃ­a.
    - [ ] Implementar la lÃ³gica incremental para actualizar el JSON de `dominio_por_tema`.
- [x] **Tarea: Conductor - User Manual Verification 'Fase 2: LÃ³gica de CÃ¡lculo (TDD)' (Protocol in workflow.md)** [manual]

## Fase 3: IntegraciÃ³n y Cierre
- [x] **Tarea: Integrar Servicio en Vistas de Actividad** [manual]
    - [ ] Llamar al servicio en `validar_respuesta` (prÃ¡ctica) despuÃ©s de guardar el resultado.
    - [ ] Llamar al servicio en `rendir_examen` (diagnÃ³stico) despuÃ©s de procesar el puntaje.
- [x] **Tarea: VerificaciÃ³n de Cobertura y Estilo** [manual]
    - [x] Asegurar >80% de cobertura en la nueva lÃ³gica de servicios.
    - [x] Validar que no se introdujeron regresiones en el flujo de guardado de resultados.
- [x] **Tarea: Conductor - User Manual Verification 'Fase 3: IntegraciÃ³n y Cierre' (Protocol in workflow.md)** [manual]
