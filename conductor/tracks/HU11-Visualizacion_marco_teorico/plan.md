# Implementation Plan: HU11 - Visualización de marco teórico

## Phase 1: Real Content Population
- [x] Task: Update `AppTutoria.models.ContenidoTema` for the "Triángulos" theme with real theoretical content (Classification by sides/angles, sum of interior angles = 180°).
- [x] Task: Conductor - User Manual Verification 'Real Content Population' (Protocol in workflow.md) [checkpoint: Phase 1 Complete]

## Phase 2: View and Logic Updates (TDD)
- [x] Task: Write failing tests in `AppTutoria/tests_views.py` to verify section-based navigation.
    - Test: Default access shows theme summary (Resumen).
    - Test: Access with `?seccion=teoria` shows detailed theoretical content.
    - Test: Access to future sections (exercises/videos) shows placeholder or forbidden status.
- [x] Task: Update the `tema_detalle` view in `AppTutoria/views.py` to handle the `seccion` query parameter.
- [x] Task: Ensure all tests pass (Green Phase).
- [x] Task: Conductor - User Manual Verification 'View and Logic Updates' (Protocol in workflow.md) [checkpoint: Phase 2 Complete]

## Phase 3: Sidebar UI and Template Integration
- [x] Task: Update `AppTutoria/templates/AppTutoria/tema_detalle.html` to implement the Sidebar UI.
    - Add Sidebar container with links for: Resumen, Marco Teórico, Ejercicios (disabled), Videos (disabled).
    - Implement conditional rendering in the content area based on the selected section.
    - Ensure a responsive and gamified design consistent with the project style.
- [x] Task: Conductor - User Manual Verification 'Sidebar UI and Template Integration' (Protocol in workflow.md) [checkpoint: Phase 3 Complete]

## Phase 4: Final Validation and Quality Gates
- [x] Task: Verify test coverage for `AppTutoria` meets the >80% requirement.
- [x] Task: Perform a final manual end-to-end check of the navigation between Resumen and Marco Teórico.
- [x] Task: Conductor - User Manual Verification 'Final Validation and Quality Gates' (Protocol in workflow.md) [checkpoint: Phase 4 Complete]
