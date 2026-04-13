# Implementation Plan - HU22 - AsignaciÃ³n de puntos por actividad

Este plan detalla los pasos para integrar el sistema de puntos en las actividades del estudiante, centralizando la lÃ³gica y asegurando el feedback visual.

## Fase 1: Backend y Persistencia
- [x] **Tarea: Extender el Modelo `Profile`**
    - [x] AÃ±adir el campo `puntos_acumulados` (PositiveIntegerField) al modelo `Profile` en `AppGestionUsuario/models.py`.
    - [x] Generar y aplicar migraciones.
- [x] **Tarea: Crear el Servicio de GamificaciÃ³n**
    - [x] Implementar un mÃ³dulo `AppGestionUsuario/services_gamification.py` con la lÃ³gica de asignaciÃ³n de puntos.
    - [x] Definir constantes para los puntajes por actividad y nivel.
- [ ] **Tarea: Conductor - User Manual Verification 'Fase 1: Backend y Persistencia' (Protocol in workflow.md)**

## Fase 2: IntegraciÃ³n de LÃ³gica (TDD)
- [x] **Tarea: Integrar Puntos en Ejercicios (TDD)**
    - [x] Escribir pruebas unitarias para validar la suma de puntos tras resolver un ejercicio (segÃºn acierto y nivel).
    - [x] Llamar al servicio en la vista `validar_respuesta` de `AppEvaluar`.
- [x] **Tarea: Integrar Puntos en Videos y TeorÃ­a**
    - [x] Escribir pruebas unitarias para evitar asignaciones duplicadas de puntos por la misma actividad.
    - [x] Integrar el servicio en las funciones de registro de visualizaciÃ³n y progreso teÃ³rico.
- [ ] **Tarea: Conductor - User Manual Verification 'Fase 2: IntegraciÃ³n de LÃ³gica (TDD)' (Protocol in workflow.md)**

## Fase 3: Frontend y Feedback
- [x] **Tarea: Implementar Notificaciones de Puntos (UI)**
    - [x] AÃ±adir lÃ³gica en las respuestas AJAX de ejercicios para incluir el total de puntos ganados.
    - [x] Implementar animaciÃ³n CSS o mensaje Toast en el frontend para mostrar la ganancia de puntos.
- [x] **Tarea: Actualizar VisualizaciÃ³n en el Perfil**
    - [x] Asegurar que el campo de puntos sea visible en la plantilla de perfil del estudiante.
- [x] **Tarea: VerificaciÃ³n Final y Cobertura**
    - [x] Ejecutar todas las pruebas del mÃ³dulo de gamificaciÃ³n y asegurar >80% de cobertura.
- [ ] **Tarea: Conductor - User Manual Verification 'Fase 3: Frontend y Feedback' (Protocol in workflow.md)**
