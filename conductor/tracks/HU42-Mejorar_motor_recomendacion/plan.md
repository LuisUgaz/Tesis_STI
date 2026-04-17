# Plan de Implementación: Mejora del Motor de Recomendación Adaptativa (HU42)

## Fase 1: Preparación de Datos y Modelos
En esta fase, prepararemos la infraestructura de datos necesaria para capturar el tiempo de respuesta.

- [x] **Task: Modificar el modelo RespuestaUsuario**
    - [x] Crear test que verifique la existencia del campo `tiempo_respuesta` (float).
    - [x] Añadir el campo `tiempo_respuesta` al modelo en `AppEvaluar/models.py`.
    - [x] Ejecutar migraciones.
- [x] **Task: Actualizar el formulario y vista del examen**
    - [x] Escribir tests para asegurar que el tiempo enviado desde el frontend se guarde.
    - [x] Modificar la vista de guardado de respuestas en `AppEvaluar/views.py`.
- [x] **Task: Conductor - User Manual Verification 'Fase 1' (Protocol in workflow.md)**

## Fase 2: Algoritmo de Puntaje de Desempeño Ponderado (PDP)
Implementación de la lógica matemática para evaluar debilidades basadas en dificultad y tiempo.

- [x] **Task: Implementar lógica de ponderación por dificultad (3-2-1)**
    - [x] Crear tests unitarios en `AppEvaluar/tests_adaptive_logic.py` con diferentes escenarios de dificultad.
    - [x] Actualizar la función `calcular_recomendacion` en `AppEvaluar/services.py` para usar el peso lineal.
- [x] **Task: Implementar penalización por tiempo estadístico**
    - [x] Crear tests que simulen tiempos altos en respuestas correctas.
    - [x] Implementar el cálculo del promedio y desviación estándar para normalizar el tiempo.
- [x] **Task: Conductor - User Manual Verification 'Fase 2' (Protocol in workflow.md)**

## Fase 3: Integración de Clasificador SVM
Integración de `scikit-learn` para resolver empates de forma inteligente.

- [x] **Task: Integrar scikit-learn y configurar el modelo SVM**
    - [x] Escribir tests que fuercen un empate en el PDP de dos temas.
    - [x] Implementar la clase/función del clasificador SVM dentro de `AppEvaluar/services.py`.
    - [x] Asegurar que el SVM use las features: `tiempo_promedio_global`, `nivel_perfil`, `puntos`.
- [x] **Task: Implementar lógica de Fallback**
    - [x] Testear comportamiento cuando no hay datos suficientes para el SVM.
    - [x] Implementar retorno al orden alfabético si el clasificador falla.
- [x] **Task: Conductor - User Manual Verification 'Fase 3' (Protocol in workflow.md)**

## Fase 4: Integración con Ajuste de Dificultad (HU15)
Asegurar que el nuevo puntaje actualice correctamente el perfil del estudiante.

- [x] **Task: Actualizar HU15 con el nuevo PDP**
    - [x] Testear que el `profile.nivel_dificultad_actual` cambie según el nuevo puntaje ponderado.
    - [x] Ajustar los rangos (0-40, 41-75, 76-100) para que operen sobre el PDP.
- [x] **Task: Pruebas de Regresión y Cobertura**
    - [x] Ejecutar suite completa de tests de la AppEvaluar.
    - [x] Verificar cobertura > 80% en los nuevos servicios.
- [x] **Task: Conductor - User Manual Verification 'Fase 4' (Protocol in workflow.md)**
