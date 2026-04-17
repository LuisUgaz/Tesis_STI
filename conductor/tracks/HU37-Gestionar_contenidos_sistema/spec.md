# Specification: HU37 - Gestionar contenidos del sistema

## 1. Overview
The goal of this track is to provide administrators with a centralized dashboard to manage general system content and global configurations. This includes the ability to update institutional information, contact details, and static page content (like the Home page or an \"About Us\" section) without directly modifying the code or the standard Django Admin interface.

## 2. Functional Requirements

### 2.1 Admin Dashboard for Content
- A dedicated, protected view for users with the **Administrador** role.
- Sidebar or top navigation link leading to this \"Gestionar Contenidos\" dashboard.

### 2.2 Global Configuration Management
- A section to update:
    - **Nombre del Sistema/Colegio:** The main name shown in the navbar and page titles.
    - **Email de Contacto Docente:** The destination email for student inquiries (currently hardcoded in settings).
    - **Texto del Footer:** A customizable footer text (e.g., copyright, institution credits).
- Real-time impact: Once saved, these values should reflect across the entire application via a global context processor.

### 2.3 Static Page Management
- Ability to manage at least two initial pages: **Inicio (Home)** and **Nosotros (About)**.
- Each page should have:
    - **Título:** Displayed as the page heading.
    - **Slug:** Unique identifier for the URL (e.g., `inicio`, `nosotros`).
    - **Contenido HTML:** The body of the page, managed via a **WYSIWYG editor** (e.g., CKEditor or similar lightweight integration).
- Implementation: The current `home.html` will be updated to display the content from the database for the `inicio` slug.

### 2.4 Access Control
- Access restricted strictly to users with `profile.rol == 'Administrador'`.
- Use `AdminRequiredMixin` (already existing in `AppGestionUsuario/views.py`) for all related views.

## 3. Technical Requirements

### 3.1 Data Models
- **`ConfiguracionGlobal` (Singleton):**
    - `nombre_sistema` (CharField)
    - `email_contacto` (EmailField)
    - `texto_footer` (TextField)
- **`PaginaEstatica`:**
    - `titulo` (CharField)
    - `slug` (SlugField, unique)
    - `contenido_html` (TextField)
    - `ultima_actualizacion` (DateTimeField)

### 3.2 Frontend Integration
- **WYSIWYG Editor:** Integrate a JavaScript-based editor (like CKEditor 5 or Quill) in the admin forms for static page content.
- **Context Processor:** Create a Django context processor to inject `ConfiguracionGlobal` data into every template.

### 3.3 Persistence & Logic
- All operations (Create/Update) must be performed via custom Django forms and views.
- Validations to ensure required fields and unique slugs.

## 4. Acceptance Criteria
- [ ] Admin can log in and access the \"Gestión de Contenidos\" dashboard.
- [ ] Admin can update the system name, and it changes in the Navbar immediately.
- [ ] Admin can update the contact email, and student inquiries reach the new email.
- [ ] Admin can edit the Home page content using a visual editor, and the changes appear on the home screen.
- [ ] Non-admin users are blocked from accessing these management views.

## 5. Out of Scope
- Full-featured CMS with menu builders or media galleries (beyond basic images in the editor).
- Management of pedagogical content (already handled in specialized HUs).
