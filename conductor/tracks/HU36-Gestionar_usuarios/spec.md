# Track Specification - HU36 - Gestionar usuarios

## 1. Overview
Esta funcionalidad permite a los administradores del sistema gestionar de manera centralizada las cuentas de usuario de la plataforma Tesis STI. El objetivo es proporcionar una interfaz robusta para listar, filtrar, crear, editar y desactivar usuarios (Estudiantes, Docentes y otros Administradores) para mantener actualizado el acceso al sistema.

## 2. Functional Requirements
- **Módulo de Administración de Usuarios:**
    - Accesible exclusivamente para usuarios con el rol `Administrador` en su perfil (`Profile`).
    - Listado dinámico de todos los usuarios registrados en el sistema.
- **Capacidades de Listado y Filtrado:**
    - **Búsqueda de Texto:** Filtrado por nombre de usuario, nombres o apellidos.
    - **Filtro por Rol:** Segmentación por Estudiante, Docente o Administrador.
    - **Filtro por Grado/Sección:** Específico para el rol Estudiante.
    - **Filtro por Estado:** Filtrar entre usuarios activos e inactivos.
- **Gestión de Cuentas (CRUD):**
    - **Creación:** Formulario para registrar nuevos usuarios capturando datos básicos del `User` y del `Profile`.
    - **Edición:** Actualización de datos personales, correo electrónico y grado/sección.
    - **Password Temporal:** Funcionalidad para asignar o resetear una contraseña temporal.
    - **Cambio de Rol:** Capacidad del administrador para modificar el rol asignado a un usuario existente.
    - **Email Único:** Validación estricta para asegurar que no se dupliquen correos en el sistema.
- **Desactivación de Usuarios:**
    - Implementación de un **Toggle Rápido** (asíncrono/AJAX) en el listado para activar o desactivar usuarios instantáneamente sin recargar la página.

## 3. Non-Functional Requirements
- **Seguridad de Acceso:** Restricción total mediante decoradores de Django o mixins que validen el rol `Administrador` del usuario logueado.
- **Interactividad:** Uso de AJAX para la desactivación rápida para mejorar la experiencia del administrador.
- **Idioma:** Toda la interfaz, mensajes de validación y documentación deben estar en español.
- **Consistencia:** Reutilización de modelos existentes (`User` y `Profile`) evitando duplicar lógica de autenticación.

## 4. Acceptance Criteria
- **Escenario: Acceso Restringido**
    - **Dado** que un estudiante o docente intenta acceder a la URL del módulo de usuarios.
    - **Entonces** el sistema debe denegar el acceso (Error 403) o redirigir al home con un mensaje de advertencia.
- **Escenario: Gestión Completa**
    - **Dado** que el administrador accede al módulo.
    - **Cuando** registra un nuevo docente con email único y contraseña temporal.
    - **Entonces** el usuario debe crearse correctamente en las tablas `auth_user` y `AppGestionUsuario_profile`.
- **Escenario: Desactivación Rápida**
    - **Dado** que el administrador visualiza la lista de usuarios.
    - **Cuando** pulsa el toggle de desactivación de un estudiante.
    - **Entonces** el sistema debe marcar al usuario como inactivo (`is_active = False`) de forma asíncrona.

## 5. Out of Scope
- Flujos avanzados de recuperación de contraseña por parte del usuario (auto-servicio).
- Gestión de permisos granulares por módulo individual.
- Reportes de actividad detallados por usuario (logs de auditoría).
