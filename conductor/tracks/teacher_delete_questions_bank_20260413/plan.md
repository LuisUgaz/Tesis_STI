# Plan de Implementación: HU31 - Eliminar Preguntas del Banco

## Fase 1: Actualización de Modelos y Pruebas (Red Phase)
- [x] Task: Actualizar el modelo Ejercicio para soportar eliminación lógica.
    - [x] Añadir campo `es_activo = models.BooleanField(default=True)` a `AppEvaluar.Ejercicio`.
    - [x] Generar y ejecutar migraciones (`makemigrations`, `migrate`).
- [x] Task: Crear pruebas unitarias para la eliminación de ejercicios.
    - [x] Actualizar `AppEvaluar/tests_banco_preguntas.py` con pruebas para la eliminación lógica.
    - [x] Definir prueba para validar que una pregunta marcada como inactiva no se lista en la gestión.
    - [x] Definir prueba para validar que una pregunta inactiva no aparece en las sesiones de práctica.
    - [x] Definir prueba de acceso restringido (solo docentes).
- [x] Task: Ejecutar pruebas y confirmar que fallan (Fase Roja).
- [x] Task: Conductor - User Manual Verification 'Actualización de Modelos y Pruebas' (Protocolo en workflow.md)

## Fase 2: Implementación de la Lógica de Eliminación (Green Phase)
- [x] Task: Desarrollar la vista de eliminación lógica.
    - [x] Crear `BancoPreguntasDeleteView` en `AppEvaluar/views.py`.
    - [x] Implementar la lógica para cambiar `es_activo` a `False` en lugar de borrar.
    - [x] Registrar la ruta en `AppEvaluar/urls.py` (`banco-preguntas/eliminar/<int:pk>/`).
- [x] Task: Ajustar filtrado en vistas existentes.
    - [x] Modificar `BancoPreguntasListView` para mostrar solo preguntas activas por defecto.
    - [x] Modificar la lógica de selección de ejercicios en la práctica del estudiante para excluir inactivos.
- [x] Task: Ejecutar pruebas y confirmar que pasan (Fase Verde).
- [x] Task: Conductor - User Manual Verification 'Implementación de la Lógica de Eliminación' (Protocolo en workflow.md)

## Fase 3: Interfaz de Usuario e Integración
- [x] Task: Integrar el mecanismo de confirmación en el listado.
    - [x] Actualizar `AppEvaluar/templates/AppEvaluar/banco_preguntas_list.html` con el botón de eliminar y el modal de confirmación de Bootstrap.
    - [x] Añadir lógica JavaScript para pasar el ID de la pregunta al modal dinámicamente.
- [x] Task: Verificación final de flujo completo.
    - [x] Realizar pruebas manuales de eliminación y verificar persistencia en la base de datos (PostgreSQL).
    - [x] Confirmar que no se rompe la integridad referencial con resultados antiguos.
- [x] Task: Conductor - User Manual Verification 'Interfaz de Usuario e Integración' (Protocolo en workflow.md)
