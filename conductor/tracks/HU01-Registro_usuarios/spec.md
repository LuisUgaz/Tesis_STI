# Especificación de Pista: Registro de Usuarios (HU01)

## Descripción General
Esta pista implementa la Historia de Usuario HU01: "Registro de Usuarios". El objetivo es permitir que los nuevos usuarios (principalmente estudiantes) se registren en la plataforma "Sistema Tutor Inteligente Adaptativo para Geometría" (Tesis STI). El registro capturará datos básicos y extendidos, con un enfoque visual gamificado y juvenil.

## Requisitos Funcionales

1.  **Formulario de Registro:**
    *   **Campos Obligatorios:** Nombre de Usuario (único), Correo Electrónico (único y formato válido), Contraseña (fuerte), Confirmar Contraseña, Nombre y Apellidos completos.
    *   **Campos Condicionales:** Grado y Sección (solo para estudiantes).
2.  **Validaciones del Servidor:**
    *   Unicidad de Usuario y Correo.
    *   Coincidencia de Contraseñas.
    *   Contraseña Fuerte: Mínimo 8 caracteres, números y símbolos.
    *   Campos obligatorios completos.
3.  **Persistencia:**
    *   Los datos se guardarán en la base de datos PostgreSQL.
    *   Se creará el usuario estándar de Django y un perfil extendido (Profile) en la aplicación `AppGestionUsuario`.
4.  **Gestión de Roles:**
    *   Por defecto, los usuarios registrados mediante este formulario tendrán el rol de **Estudiante**.
    *   La asignación de otros roles (Docente, Admin) será manual por un Administrador desde el panel de Django Admin.
5.  **Interfaz de Usuario (UI):**
    *   Estilo visual **Gamificado / Juvenil**, alineado con la visión del producto para estudiantes de secundaria.
    *   Uso de mensajes de éxito ("Registro exitoso") y error (ej. "El usuario ya existe").

## Requisitos No Funcionales
*   **Seguridad:** Cifrado de contraseñas mediante el sistema estándar de Django.
*   **Modularidad:** Código organizado en `AppGestionUsuario` (Modelos, Vistas, Forms).
*   **Consistencia:** Alineación con los estándares de codificación de Django y PostgreSQL.

## Criterios de Aceptación

### Escenario: Registro exitoso
*   **Dado** que el usuario se encuentra en el formulario de registro.
*   **Cuando** ingresa todos los campos obligatorios correctamente y confirma la contraseña.
*   **Entonces** el sistema debe crear la cuenta y mostrar un mensaje de éxito.

### Escenario: Usuario duplicado
*   **Dado** que el usuario se encuentra en el formulario de registro.
*   **Cuando** ingresa un nombre de usuario ya existente.
*   **Entonces** el sistema debe rechazar el registro y mostrar un mensaje indicando que el usuario ya existe.

### Escenario: Contraseñas no coinciden
*   **Dado** que el usuario se encuentra en el formulario de registro.
*   **Cuando** ingresa contraseñas diferentes.
*   **Entonces** el sistema no debe crear la cuenta y debe mostrar un mensaje de validación.

## Fuera de Alcance
*   Inicio de sesión automático después del registro.
*   Redirección automática por rol.
*   Recuperación de contraseña.
*   Verificación por correo electrónico.
