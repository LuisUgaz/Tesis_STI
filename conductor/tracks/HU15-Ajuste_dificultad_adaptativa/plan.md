# Plan de Implementación: HU15 - Ajuste de dificultad adaptativa

## Fase 1: Base de Datos y Modelo de Usuario
- [x] Task: Añadir el campo `nivel_dificultad_actual` al modelo `Profile` en `AppGestionUsuario/models.py` con opciones ('Básico', 'Intermedio', 'Avanzado') y valor por defecto 'Básico'.
- [x] Task: Actualizar el administrador de `Profile` para mostrar y permitir editar este campo.
- [x] Task: Generar y aplicar las migraciones.
- [x] Task: Conductor - User Manual Verification 'Fase 1: Base de Datos y Modelo de Usuario' (Protocol in workflow.md)

## Fase 2: Lógica de Nivel Inicial (Diagnóstico)
- [x] Task: Implementar lógica en `AppEvaluar/services.py` (o donde se procesen resultados) para asignar el nivel inicial basado en el puntaje del diagnóstico.
- [x] Task: Crear pruebas unitarias para validar la asignación de nivel inicial según diferentes rangos de puntaje.
- [x] Task: Conductor - User Manual Verification 'Fase 2: Lógica de Nivel Inicial' (Protocol in workflow.md)

## Fase 3: Lógica de Ajuste Adaptativo (Sesiones)
- [x] Task: Crear un servicio `ajustar_dificultad_estudiante` que analice los últimos `ResultadoEjercicio` de una sesión y actualice el `Profile`.
- [x] Task: Integrar la llamada a este servicio al finalizar la sesión de práctica en la vista correspondiente (o vía AJAX al terminar el último ejercicio).
- [x] Task: Escribir pruebas unitarias (TDD) para la regla del 80% de aciertos.
- [x] Task: Conductor - User Manual Verification 'Fase 3: Lógica de Ajuste Adaptativo' (Protocol in workflow.md)

## Fase 4: Integración con Práctica
- [x] Task: Modificar la lógica de selección de ejercicios en `iniciar_practica` (`AppEvaluar/views.py`) para filtrar por el nivel almacenado en el perfil.
- [x] Task: Realizar una prueba de integración completa: Rendir diagnóstico -> Ver Nivel -> Resolver Práctica -> Verificar Cambio de Nivel.
- [x] Task: Conductor - User Manual Verification 'Fase 4: Integración con Práctica' (Protocol in workflow.md)
