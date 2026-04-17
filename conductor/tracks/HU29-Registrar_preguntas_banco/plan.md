# Plan de Implementación: HU29 - Registrar Preguntas en Banco

## Fase 1: Pruebas Iniciales (Red Phase)
- [x] Task: Crear pruebas unitarias para el registro de ejercicios.
    - [x] Crear archivo `AppEvaluar/tests_banco_preguntas.py`.
    - [x] Definir pruebas para validar el acceso restringido a docentes.
    - [x] Definir pruebas para la validación de campos obligatorios en el formulario.
    - [x] Definir pruebas para el guardado exitoso de un ejercicio con sus 5 opciones.
- [x] Task: Ejecutar pruebas y confirmar que fallan (Fase Roja).
- [x] Task: Conductor - User Manual Verification 'Pruebas Iniciales' (Protocolo en workflow.md)

## Fase 2: Implementación del Backend (Green Phase)
- [x] Task: Desarrollar la lógica de formularios y vistas.
    - [x] Crear `EjercicioForm` en `AppEvaluar/forms.py`.
    - [x] Implementar un `InlineFormSet` para gestionar las 5 opciones de respuesta.
    - [x] Crear la vista `BancoPreguntasCreateView` en `AppEvaluar/views.py`.
    - [x] Registrar la nueva ruta en `AppEvaluar/urls.py`.
- [x] Task: Ejecutar pruebas y confirmar que pasan (Fase Verde).
- [x] Task: Conductor - User Manual Verification 'Implementación del Backend' (Protocolo en workflow.md)

## Fase 3: Interfaz de Usuario e Integración
- [x] Task: Crear la interfaz de registro de preguntas.
    - [x] Diseñar el template `AppEvaluar/templates/AppEvaluar/banco_preguntas_form.html` siguiendo el estilo del panel docente.
    - [x] Integrar el formulario dinámico para las 5 opciones.
    - [x] Añadir enlace de acceso al Banco de Preguntas en la navegación del docente.
- [x] Task: Verificación final de flujo completo.
    - [x] Realizar pruebas manuales de registro con diferentes temas y dificultades.
    - [x] Validar que los ejercicios guardados aparezcan en las sesiones de práctica de estudiantes.
- [x] Task: Conductor - User Manual Verification 'Interfaz de Usuario e Integración' (Protocolo en workflow.md)
