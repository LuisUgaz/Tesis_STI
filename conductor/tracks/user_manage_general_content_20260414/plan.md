# Implementation Plan: HU37 - Gestionar contenidos del sistema

## Phase 1: Models and Foundation
Implement the data models for global configurations and static pages.

- [x] Task: Create `ConfiguracionGlobal` and `PaginaEstatica` models in `AppGestionUsuario`.
    - [x] Write unit tests in `AppGestionUsuario/tests_general_content_models.py`.
    - [x] Implement models with appropriate fields (Singleton pattern for Config).
    - [x] Run migrations.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Models and Foundation' (Protocol in workflow.md)

## Phase 2: Administrative Dashboard & Forms
Create the UI for managing these contents, restricted to administrators.

- [x] Task: Create Forms for Global Config and Static Pages.
    - [x] Write tests for forms in `AppGestionUsuario/tests_general_content_forms.py`.
    - [x] Implement `ConfiguracionGlobalForm` and `PaginaEstaticaForm`.
- [x] Task: Implement Dashboard View and URL.
    - [x] Write tests for the dashboard view (access control, listing) in `AppGestionUsuario/tests_general_content_views.py`.
    - [x] Implement `AdminContentDashboardView`.
    - [x] Register URL in `AppGestionUsuario/urls.py`.
- [x] Task: Create Dashboard Templates with WYSIWYG integration.
    - [x] Create `admin_content_dashboard.html`.
    - [x] Create `admin_pagina_edit.html` with CKEditor/Quill integration.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Administrative Dashboard & Forms' (Protocol in workflow.md)

## Phase 3: Global Integration & Context Processor
Make the configuration available everywhere and update the Home page.

- [x] Task: Implement Context Processor for Global Configurations.
    - [x] Write tests for the context processor.
    - [x] Create `AppGestionUsuario/context_processors.py`.
    - [x] Register in `settings.py`.
- [x] Task: Update Base and Home templates to use dynamic content.
    - [x] Update `templates/home.html` to pull from `PaginaEstatica` (slug='inicio').
    - [x] Update Navbar/Footer to use `ConfiguracionGlobal`.
- [x] Task: Update `DOCENTE_EMAIL_DESTINO` logic in `ContactoView`.
    - [x] Refactor `ContactoView` to use the email from `ConfiguracionGlobal`.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Global Integration & Context Processor' (Protocol in workflow.md)

## Phase 4: Final Validation and Cleanup
Ensure everything is working as expected and follow the quality gates.

- [x] Task: Final system-wide verification of the new management module.
- [x] Task: Conductor - User Manual Verification 'Phase 4: Final Validation and Cleanup' (Protocol in workflow.md)
