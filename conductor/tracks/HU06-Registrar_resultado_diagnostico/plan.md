# Implementation Plan: HU06 - Registrar resultado diagnóstico

## Phase 1: Data Model & Migrations [checkpoint: MANUAL]
- [x] Task: Definir modelo `ResultadoDiagnostico` en `AppEvaluar/models.py`.
    - [x] Crear el modelo con campos: `estudiante` (FK a User), `examen` (FK a ExamenDiagnostico), `puntaje` (Decimal), `fecha_realizacion` (DateTimeField).
- [x] Task: Generar y aplicar migraciones.
    - [x] Ejecutar `python manage.py makemigrations AppEvaluar`.
    - [x] Ejecutar `python manage.py migrate`.
- [x] Task: Registrar el nuevo modelo en `admin.py`.
- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Scoring Logic & Persistence Service [checkpoint: MANUAL]
- [x] Task: Implementar lógica de cálculo de puntaje.
    - [x] Crear pruebas unitarias para el cálculo (TDD).
    - [x] Implementar función/método para validar respuestas y obtener el porcentaje.
- [x] Task: Implementar validación de intento único.
    - [x] Crear pruebas para verificar que un usuario no puede registrar dos resultados para el mismo examen.
    - [x] Implementar lógica de validación.
- [x] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: View Integration & Flow [checkpoint: MANUAL]
- [x] Task: Actualizar la vista `rendir_examen` (o la vista de procesamiento) para manejar el POST de resultados.
    - [x] Crear pruebas de integración para el envío del formulario (TDD).
    - [x] Implementar la captura de datos del POST, cálculo y guardado en `ResultadoDiagnostico`.
- [x] Task: Implementar redirección y mensajes de éxito/error.
    - [x] Redirigir a la página de resultados después de guardar satisfactoriamente.
    - [x] Mostrar mensaje de error si el usuario ya realizó el diagnóstico.
- [x] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4: Final Validation & Cleanup [checkpoint: MANUAL]
- [x] Task: Ejecutar suite completa de pruebas.
- [x] Task: Verificar persistencia directamente en PostgreSQL.
- [x] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)
