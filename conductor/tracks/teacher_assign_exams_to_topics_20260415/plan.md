# Implementation Plan (HU41): Asignar exámenes a temas

## Phase 1: Modelo de Datos y Formularios
- [x] Task: Verificar el modelo `Examen` en `AppEvaluar/models.py`. Asegurar que tiene un campo `ForeignKey` hacia `AppTutoria.Tema`. (verified)
- [x] Task: Crear o actualizar un formulario `ExamenForm` en `AppEvaluar/forms.py` que incluya el campo `tema`. (passed)
- [x] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Gestión Docente (Asignación)
- [x] Task: Implementar o actualizar `ExamenUpdateView` en `AppEvaluar/views.py`. (passed)
- [~] Task: Actualizar el template `AppEvaluar/examen_form.html` para permitir la edición y selección del tema.
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Visualización Estudiante
- [ ] Task: Modificar la vista `tema_detalle` en `AppTutoria/views.py` para consultar y enviar los exámenes asociados al contexto.
- [ ] Task: Actualizar el template `AppTutoria/templates/AppTutoria/tema_detalle.html` para mostrar una sección de 'Evaluaciones del Tema'.
- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4: Validación y Pruebas
- [ ] Task: Crear pruebas unitarias en `AppEvaluar/tests_examen_logic.py` para validar la asignación correcta.
- [ ] Task: Verificar que al eliminar un examen, las preguntas queden disponibles (como se definió en la HU39).
- [ ] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)
