# Plan de Implementación - HU44: Validación de Acceso y Redirección

## Fase 1: Ajustes en el Backend (Vistas y Lógica)
- [x] **Task: Modificar permisos en `tema_detalle`**
    - [x] Actualizar `AppTutoria/views.py`: reemplazar `PermissionDenied` por `redirect('tutoria:lista_temas')` con un mensaje flash.
    - [x] Asegurar que el mensaje use una etiqueta identificable (ej. `needs_exam`).
- [x] **Task: Validar acceso en otras vistas de contenido**
    - [x] Revisar `video_list` y aplicar la misma lógica de redirección amigable.

## Fase 2: Implementación de la Interfaz (Modal y JS)
- [x] **Task: Crear estructura HTML del Modal**
    - [x] Modificar `AppTutoria/templates/AppTutoria/lista_temas.html`.
    - [x] Añadir contenedor de modal con botón de cierre y botón de acción al examen.
- [x] **Task: Estilos y Animaciones**
    - [x] Implementar CSS para el esquema "Info Blue".
    - [x] Añadir efectos de difuminado de fondo y entrada suave del modal.
- [x] **Task: Lógica de Activación Vanilla JS**
    - [x] Implementar script para detectar el mensaje de Django al cargar la página.
    - [x] Añadir `EventListeners` a los enlaces de temas bloqueados para disparar el modal.

## Fase 3: Validación y Pruebas
- [x] **Task: Pruebas de Flujo Completo**
    - [x] Verificar redirección desde URL directa.
    - [x] Verificar bloqueo de clics en la lista.
    - [x] Confirmar que el botón "Rendir Examen" redirige correctamente al ID 1.
- [x] **Task: Conductor - User Manual Verification 'Validación de Acceso Amigable' (Protocol in workflow.md)**
