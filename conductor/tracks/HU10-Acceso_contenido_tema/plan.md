# Implementation Plan: HU10 - Acceso a contenido de tema

## Phase 1: Data Model Updates
- [x] Task: Update `AppTutoria.models.Tema` to include a `slug` field (unique=True).
- [x] Task: Create `AppTutoria.models.ContenidoTema` with fields: `tema` (FK to Tema), `cuerpo_html` (TextField), and `material_pdf` (FileField, optional).
- [x] Task: Generate and run migrations for `AppTutoria`.
- [x] Task: Populate some initial data (at least one `Tema` with `ContenidoTema`) to test the flow.
- [x] Task: Conductor - User Manual Verification 'Data Model Updates' (Protocol in workflow.md) [checkpoint: Phase 1 Complete]

## Phase 2: View and URL Implementation
- [x] Task: Write failing tests for `tema_detalle` view in `AppTutoria/tests_views.py`.
    - Test: Access for unauthenticated users (Redirect).
    - Test: Access for non-students (Forbidden).
    - Test: Access for non-recommended themes (Forbidden/Redirect).
    - Test: Successful access for a recommended theme.
- [x] Task: Implement `tema_detalle` view in `AppTutoria/views.py`.
    - Check if theme exists by slug.
    - Check if user is authenticated and is a 'Estudiante'.
    - Check if the theme is recommended for the user (using `RecomendacionEstudiante`).
- [x] Task: Register the URL in `AppTutoria/urls.py` using `<slug:slug>/`.
- [x] Task: Ensure all tests pass (Green Phase).
- [x] Task: Conductor - User Manual Verification 'View and URL Implementation' (Protocol in workflow.md) [checkpoint: Phase 2 Complete]

## Phase 3: Template and UI Integration
- [x] Task: Create `AppTutoria/templates/AppTutoria/tema_detalle.html`.
    - Display theme name.
    - Render `cuerpo_html` safely (using `|safe` filter).
    - Provide a "Volver a la lista" button.
- [x] Task: Update `AppTutoria/templates/AppTutoria/lista_temas.html` to link theme items to their detail page.
- [x] Task: Conductor - User Manual Verification 'Template and UI Integration' (Protocol in workflow.md) [checkpoint: Phase 3 Complete]

## Phase 4: Final Validation and Quality Gates
- [x] Task: Verify test coverage for `AppTutoria` is > 80%.
- [x] Task: Run manual verification of the end-to-end flow.
- [x] Task: Conductor - User Manual Verification 'Final Validation and Quality Gates' (Protocol in workflow.md) [checkpoint: Phase 4 Complete]
