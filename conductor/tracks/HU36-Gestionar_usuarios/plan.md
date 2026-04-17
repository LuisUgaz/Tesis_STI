# Implementation Plan - HU36 - Gestionar usuarios

Este plan detalla la implementación del módulo administrativo para la gestión centralizada de usuarios en la plataforma Tesis STI.

## Fase 1: Vistas y Formularios CRUD
- [x] Task: Crear `AdminRequiredMixin` en `AppGestionUsuario/views.py` para restringir el acceso basado en el rol de `Administrador` del perfil.
- [x] Task: Desarrollar `AdminUserForm` en `AppGestionUsuario/forms.py` para la creación y edición de usuarios, integrando los modelos `User` y `Profile`.
    - [x] Implementar validación de Email Único.
    - [x] Añadir campo para Password Temporal.
- [x] Task: Implementar `UserManagementListView` con lógica de filtrado dinámico (Búsqueda, Rol, Grado/Sección, Estado).
- [x] Task: Crear `UserManagementCreateView` y `UserManagementUpdateView` para el CRUD de usuarios.
- [x] Task: Configurar las rutas correspondientes en `AppGestionUsuario/urls.py`.
- [ ] Task: Conductor - User Manual Verification 'Fase 1: Vistas y Formularios CRUD' (Protocol in workflow.md)

## Fase 2: Interactividad y Desactivación
- [x] Task: Desarrollar la plantilla `AppGestionUsuario/admin_user_list.html` con una tabla interactiva y filtros de Bootstrap 5.
- [x] Task: Implementar la vista `UserToggleStatusView` que procese peticiones AJAX para activar/desactivar usuarios (`is_active`).
- [x] Task: Añadir script de JavaScript (Vanilla) para manejar el Toggle Rápido y actualizaciones asíncronas en el listado.
- [ ] Task: Conductor - User Manual Verification 'Fase 2: Interactividad y Desactivación' (Protocol in workflow.md)

## Fase 3: Integración y Validación
- [x] Task: Añadir el enlace "Gestionar Usuarios" en la Navbar de `templates/home.html`, visible solo para usuarios con el rol `Administrador`.
- [x] Task: Crear las plantillas para creación y edición (`admin_user_form.html`).
- [x] Task: Realizar pruebas unitarias e integración en `AppGestionUsuario/tests_admin_user.py`:
    - [x] Probar restricción de acceso (Administrador vs Otros).
    - [x] Verificar creación y edición de usuarios (User + Profile).
    - [x] Validar el funcionamiento del Toggle Rápido de estado.
- [ ] Task: Conductor - User Manual Verification 'Fase 3: Integración y Validación' (Protocol in workflow.md)
