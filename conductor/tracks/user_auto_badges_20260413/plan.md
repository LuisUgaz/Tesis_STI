# Implementation Plan - HU24 - Asignación automática de insignias

Este plan detalla la integración de un sistema de logros basado en insignias para incentivar el progreso académico.

## Fase 1: Backend y Persistencia
- [x] **Tarea: Modelos de GamificaciÃ³n Extendidos**
    - [x] Crear el modelo `Insignia` en `AppGestionUsuario/models.py`.
    - [x] Crear el modelo `LogroEstudiante` para la relaciÃ³n muchos a muchos.
    - [x] Generar y aplicar migraciones.
    - [x] Crear una migraciÃ³n de datos (o fixture) con un set inicial de 3-4 insignias bÃ¡sicas.
- [ ] **Tarea: Conductor - User Manual Verification 'Fase 1: Backend y Persistencia' (Protocol in workflow.md)**

## Fase 2: Motor de Reglas (TDD)
- [x] **Tarea: Implementar Evaluador de Logros en GamificationService (TDD)**
    - [x] Escribir pruebas unitarias para validar que se asigne la insignia "Bienvenida" tras la primera actividad.
    - [x] Escribir pruebas para el otorgamiento por dominio (precisiÃ³n > 80%).
    - [x] Escribir pruebas para evitar asignaciones duplicadas de la misma insignia.
    - [x] Implementar el mÃ©todo `check_and_assign_badges` en el servicio centralizado.
- [ ] **Tarea: Conductor - User Manual Verification 'Fase 2: Motor de Reglas (TDD)' (Protocol in workflow.md)**

## Fase 3: Frontend y Feedback Visual
- [x] **Tarea: Notificaciones de Insignias (UI)**
    - [x] Modificar la respuesta AJAX de ejercicios para incluir una lista de `nuevas_insignias` obtenidas.
    - [x] Implementar un Toast especial en el frontend para anunciar el logro con icono.
- [x] **Tarea: GalerÃ­a de Insignias en Perfil**
    - [x] Actualizar `profile.html` para mostrar la cuadrÃ­cula de insignias obtenidas.
    - [x] Estilizar las insignias con iconos representativos.
- [x] **Tarea: VerificaciÃ³n Final y Cobertura**
    - [x] Ejecutar todas las pruebas del mÃ³dulo de insignias y asegurar >80% de cobertura.
- [ ] **Tarea: Conductor - User Manual Verification 'Fase 3: Frontend y Feedback Visual' (Protocol in workflow.md)**
