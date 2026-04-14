# Plan de Implementación: HU34 - Eliminar videos recomendados

## Fase 1: Modificación de Modelos y Base de Datos
- [x] Tarea: Escribir pruebas unitarias (Red) verificando que el modelo `VideoTema` tenga el campo `es_activo` y que por defecto sea `True`.
- [x] Tarea: Añadir el campo `es_activo = models.BooleanField(default=True)` al modelo `VideoTema` en `AppTutoria/models.py`.
- [x] Tarea: Generar y aplicar las migraciones de la base de datos para `AppTutoria` (Green).
- [x] Tarea: Refactorizar y asegurar cobertura.
- [x] Tarea: Conductor - User Manual Verification 'Fase 1: Modificación de Modelos y Base de Datos' (Protocol in workflow.md)

## Fase 2: Lógica de Negocio (Backend)
- [x] Tarea: Escribir pruebas unitarias (Red) para una nueva vista de eliminación, verificando el borrado lógico (`es_activo=False`), restricción de rol (Docente/Admin) y filtros en vistas existentes.
- [x] Tarea: Crear una nueva vista `VideoTemaSoftDeleteView` (o similar) en `AppTutoria/views.py` para manejar el borrado lógico (POST).
- [x] Tarea: Añadir la nueva ruta en `AppTutoria/urls.py` (ej: `/gestion/videos/<int:pk>/eliminar/`).
- [x] Tarea: Modificar `VideoTemaListView` y `video_list` en `AppTutoria/views.py` para filtrar y mostrar solo los videos activos (`es_activo=True`) (Green).
- [x] Tarea: Refactorizar y asegurar seguridad (LoginRequiredMixin, TeacherRequiredMixin).
- [x] Tarea: Conductor - User Manual Verification 'Fase 2: Lógica de Negocio (Backend)' (Protocol in workflow.md)

## Fase 3: Interfaz de Usuario (Frontend)
- [x] Tarea: Escribir pruebas de integración verificando la aparición del botón de eliminar en el listado de docentes y la ausencia del video para los estudiantes.
- [x] Tarea: Modificar el template `video_gestion_list.html` añadiendo una columna "Acciones" y un botón de "Eliminar".
- [x] Tarea: Implementar un modal de confirmación simple (Confirmar/Cancelar) integrado con el botón de eliminar.
- [x] Tarea: Asegurar que el sistema muestre notificaciones flash (messages) confirmando la eliminación (Green).
- [x] Tarea: Refactorizar y pulir UI.
- [x] Tarea: Conductor - User Manual Verification 'Fase 3: Interfaz de Usuario (Frontend)' (Protocol in workflow.md)