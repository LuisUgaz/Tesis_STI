# Plan de Implementación: HU39 - Gestionar exámenes por tema

## Fase 1: Actualización de Modelos y Base de Datos
- [x] Task: Actualizar el modelo `Pregunta` en `AppEvaluar/models.py` para hacer `examen` (ExamenDiagnostico) opcional y añadir `examen_tema` (ForeignKey a nuevo modelo `Examen`).
- [x] Task: Crear el modelo `Examen` en `AppEvaluar/models.py` con los campos: `nombre` (único), `tema`, `cantidad_preguntas`, `tiempo_limite`, `fecha_creacion`.
- [x] Task: Ejecutar migraciones para aplicar los cambios en la base de datos.
- [x] Task: Conductor - User Manual Verification 'Fase 1: Actualización de Modelos y Base de Datos' (Protocol in workflow.md)

## Fase 2: Lógica de Negocio y Servicios
- [x] Task: Crear pruebas unitarias en `AppEvaluar/tests_examen_logic.py` para la lógica de asignación automática de preguntas (Red Phase).
- [x] Task: Implementar el servicio de asignación aleatoria de preguntas en `AppEvaluar/services.py`, asegurando que solo se usen preguntas disponibles y del tema correcto (Green Phase).
- [x] Task: Implementar la validación de cantidad suficiente de preguntas antes de crear el examen (Green Phase).
- [x] Task: Implementar la lógica de liberación de preguntas al eliminar un examen (Green Phase).
- [x] Task: Verificar cobertura de las pruebas de lógica (>80%).
- [x] Task: Conductor - User Manual Verification 'Fase 2: Lógica de Negocio y Servicios' (Protocol in workflow.md)

## Fase 3: Interfaz del Docente y Dashboard
- [x] Task: Crear pruebas funcionales para las vistas de gestión de exámenes (Red Phase).
- [x] Task: Implementar la vista del Dashboard que muestra indicadores de preguntas disponibles por tema en `AppEvaluar/views.py`.
- [x] Task: Implementar el formulario de creación de exámenes y la acción de eliminación en `AppEvaluar/views.py`.
- [x] Task: Crear las plantillas HTML necesarias para el dashboard y el formulario de examen.
- [x] Task: Configurar las URLs correspondientes en `AppEvaluar/urls.py`.
- [x] Task: Verificar cobertura de las pruebas de vistas (>80%).
- [x] Task: Conductor - User Manual Verification 'Fase 3: Interfaz del Docente y Dashboard' (Protocol in workflow.md)

## Fase 4: Verificación Final y Cierre
- [x] Task: Realizar pruebas de integración para asegurar que el flujo completo (creación -> asignación -> eliminación -> disponibilidad) funciona correctamente.
- [x] Task: Verificar el cumplimiento de los criterios de aceptación y las guías de estilo del código.
- [x] Task: Conductor - User Manual Verification 'Fase 4: Verificación Final y Cierre' (Protocol in workflow.md)
