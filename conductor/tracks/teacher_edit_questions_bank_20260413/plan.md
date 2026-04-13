# Plan de Implementación: HU30 - Editar Preguntas del Banco

## Fase 1: Pruebas Iniciales (Red Phase)
- [x] Task: Crear pruebas unitarias para el listado y edición de ejercicios.
    - [x] Actualizar `AppEvaluar/tests_banco_preguntas.py` con pruebas para la vista de listado.
    - [x] Definir pruebas para validar el acceso restringido a docentes en el listado.
    - [x] Definir pruebas para la carga correcta de datos en el formulario de edición.
    - [x] Definir pruebas para el guardado exitoso (persistencia) de cambios en Ejercicio y sus 5 Opciones.
- [x] Task: Ejecutar pruebas y confirmar que fallan (Fase Roja).
- [x] Task: Conductor - User Manual Verification 'Pruebas Iniciales' (Protocolo en workflow.md)

## Fase 2: Implementación de Vistas y Lógica (Green Phase)
- [x] Task: Desarrollar la lógica de listado y edición en el backend.
    - [x] Crear `BancoPreguntasListView` en `AppEvaluar/views.py`.
    - [x] Crear `BancoPreguntasUpdateView` en `AppEvaluar/views.py`.
    - [x] Registrar las nuevas rutas en `AppEvaluar/urls.py` (`banco-preguntas/` y `banco-preguntas/editar/<int:pk>/`).
- [x] Task: Ejecutar pruebas y confirmar que pasan (Fase Verde).
- [x] Task: Conductor - User Manual Verification 'Implementación de Vistas y Lógica' (Protocolo en workflow.md)

## Fase 3: Interfaz de Usuario e Integración
- [x] Task: Crear las interfaces de gestión de preguntas.
    - [x] Diseñar el template `AppEvaluar/templates/AppEvaluar/banco_preguntas_list.html` con una tabla interactiva para el docente.
    - [x] Diseñar el template `AppEvaluar/templates/AppEvaluar/banco_preguntas_edit.html` específico para la edición, basándose en el formulario de creación.
    - [x] Añadir enlace de acceso al Listado del Banco de Preguntas en la navegación del docente y en el Panel Analítico.
- [x] Task: Verificación final de flujo completo.
    - [x] Realizar pruebas manuales de edición de textos, temas y opciones correctas.
    - [x] Validar la integridad de los datos persistidos en la base de datos (PostgreSQL).
- [x] Task: Conductor - User Manual Verification 'Interfaz de Usuario e Integración' (Protocolo en workflow.md)
