# Implementation Plan - HU23 - Subida de nivel

Este plan detalla los pasos para implementar el sistema de subida de nivel basado en XP, asegurando la persistencia y la retroalimentaciÃ³n visual.

## Fase 1: Backend y Persistencia
- [x] **Tarea: Extender el Modelo `Profile`**
    - [x] AÃ±adir el campo `nivel_estudiante` (PositiveIntegerField) al modelo `Profile` en `AppGestionUsuario/models.py`.
    - [x] Establecer el valor inicial (default) en 1.
    - [x] Generar y aplicar migraciones.
- [ ] **Tarea: Conductor - User Manual Verification 'Fase 1: Backend y Persistencia' (Protocol in workflow.md)**

## Fase 2: LÃ³gica de Subida de Nivel (TDD)
- [x] **Tarea: Implementar LÃ³gica de Niveles en GamificationService (TDD)**
    - [x] Escribir pruebas unitarias para validar que el nivel sube cada 100 puntos (Nivel 1 -> 2 al llegar a 100).
    - [x] Escribir pruebas para asegurar que el nivel no sube antes del umbral.
    - [x] Implementar un mÃ©todo `update_level_if_needed` en el servicio centralizado de gamificaciÃ³n.
- [ ] **Tarea: Conductor - User Manual Verification 'Fase 2: LÃ³gica de Subida de Nivel (TDD)' (Protocol in workflow.md)**

## Fase 3: IntegraciÃ³n y Feedback Visual
- [x] **Tarea: NotificaciÃ³n de Subida de Nivel (UI)**
    - [x] Modificar la respuesta AJAX de ejercicios para incluir un flag `subio_nivel` y el `nuevo_nivel`.
    - [x] Implementar un Toast especial en el frontend para mostrar la subida de nivel.
- [x] **Tarea: Actualizar VisualizaciÃ³n en UI**
    - [x] Mostrar el nivel en la cabecera de las prÃ¡cticas (`practica_ejercicio.html`).
    - [x] Mostrar el nivel con un distintivo en el perfil del estudiante (`profile.html`).
- [x] **Tarea: VerificaciÃ³n Final y Cobertura**
    - [x] Ejecutar todas las pruebas del track y asegurar >80% de cobertura.
- [ ] **Tarea: Conductor - User Manual Verification 'Fase 3: IntegraciÃ³n y Feedback Visual' (Protocol in workflow.md)**
