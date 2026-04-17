# Specification: HU38 - Gestionar insignias

## 1. Overview
The goal of this track is to provide administrators with a dedicated module to manage the badge catalog (insignias) within the \"Sistema Tutor Inteligente Adaptativo\". This involves implementing a CRUD (Create, Read, Update, Delete) interface that allows administrators to define and maintain the rewards available to students, ensuring the pedagogical and motivational alignment of the platform.

## 2. Functional Requirements

### 2.1 Badge List View (Read)
- A protected view for administrators to list all available badges in the system.
- Display key information: Name, Description, Icon (rendered), and Rule Type.
- Action buttons for \"Edit\" and \"Delete\" for each entry.
- A \"New Badge\" button to access the creation form.

### 2.2 Create/Edit Badge Form (Create/Update)
- A form to enter and modify badge data based on the existing `Insignia` model.
- Validations to ensure all required fields are filled and the name remains unique.
- Fields to manage:
    - **Nombre:** Badge name (e.g., \"Maestro de Triángulos\").
    - **Descripción:** Badge description (e.g., \"Otorgada al completar 5 ejercicios de nivel avanzado\").
    - **Icono:** CSS class for FontAwesome (e.g., \"fas fa-medal\").
    - **Tipo de Regla:** Categorization from pre-defined choices (HITOS, DOMINIO, CONSTANCIA, PROGRESION).

### 2.3 Delete Badge (Delete)
- Ability to remove a badge from the catalog.
- **Safety check:** Implement a confirmation modal or intermediate page before deletion.
- Note: Deletion should handle potential impacts on existing `LogroEstudiante` records (keeping referential integrity).

### 2.4 Access Control
- Strictly restricted to users with the **Administrador** role.
- Integration of a \"Gestionar Insignias\" link in the Admin Navbar.

## 3. Technical Requirements

### 3.1 Data Model
- Utilize the existing `Insignia` model in `AppGestionUsuario/models.py`.
- No modifications to the schema are required initially.

### 3.2 UI/UX
- Consistent design with the \"Gestión de Usuarios\" and \"Gestión de Contenidos\" modules.
- Use of Bootstrap 5 for layout, tables, and forms.
- Visual representation of the badge icon (rendering the FontAwesome class).

### 3.3 Logic & Views
- Implementation of Class-Based Views (CBV): `ListView`, `CreateView`, `UpdateView`, and `DeleteView`.
- Use of `AdminRequiredMixin` for security.
- Success messages using Django's messaging framework.

## 4. Acceptance Criteria
- [ ] Admin can access the \"Gestión de Insignias\" module from the navbar.
- [ ] Admin can create a new badge and see it immediately in the list.
- [ ] Admin can update a badge's description or icon.
- [ ] Admin can delete a badge after a confirmation step.
- [ ] Non-admin users (Students/Teachers) are blocked from these views (returning 403 or redirecting).

## 5. Out of Scope
- Automatic badge assignment logic (handled in other tracks).
- Usage metrics or statistics for badges.
- Advanced media upload (only FontAwesome classes are supported).
