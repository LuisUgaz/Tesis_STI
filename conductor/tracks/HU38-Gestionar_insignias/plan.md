# Implementation Plan: HU38 - Gestionar insignias

## Phase 1: Badge Forms and Integration
Develop the forms required to manage badges based on the existing model.

- [x] Task: Create `InsigniaForm` in `AppGestionUsuario/forms.py`.
    - [x] Write unit tests for the badge form in `AppGestionUsuario/tests_badges_forms.py`.
    - [x] Implement `InsigniaForm` with Bootstrap styling for all fields (Name, Description, Icon, Rule Type).
- [x] Task: Conductor - User Manual Verification 'Phase 1: Badge Forms and Integration' (Protocol in workflow.md)

## Phase 2: Administrative Views and URLs
Implement the logic and routing for the Badge CRUD.

- [x] Task: Develop Badge Management Views.
    - [x] Write unit tests for badge views (list, create, edit, delete, access control) in `AppGestionUsuario/tests_badges_views.py`.
    - [x] Implement `BadgeManagementListView`, `BadgeManagementCreateView`, `BadgeManagementUpdateView`, and `BadgeManagementDeleteView` using `AdminRequiredMixin`.
- [x] Task: Register Badge URLs in `AppGestionUsuario/urls.py`.
    - [x] Add paths for listing, creating, updating, and deleting badges.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Administrative Views and URLs' (Protocol in workflow.md)

## Phase 3: Templates and Global Access
Create the user interface and integrate it into the main navigation.

- [x] Task: Develop Badge Management Templates.
    - [x] Create `admin_badge_list.html` with a table view and action buttons.
    - [x] Create `admin_badge_form.html` for both creation and editing.
    - [x] Create `admin_badge_confirm_delete.html` for deletion safety.
- [x] Task: Update Admin Navbar in `templates/home.html`.
    - [x] Add the \"Gestionar Insignias\" link to the administrator's navigation menu.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Templates and Global Access' (Protocol in workflow.md)
