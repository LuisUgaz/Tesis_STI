# Plan: HU07 - Procesar resultados para recomendación

## Phase 1: Estructura y Validación de Datos
- [x] Task: Crear el módulo de servicio `services.py` en `AppEvaluar` para centralizar la lógica de recomendación.
- [x] Task: Implementar la excepción personalizada `SinResultadosError` para manejar la ausencia de datos de diagnóstico.
- [x] Task: Escribir pruebas unitarias para verificar que el servicio lanza `SinResultadosError` cuando un estudiante no tiene resultados.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Estructura y Validación de Datos' (Protocol in workflow.md)

## Phase 2: Lógica del Algoritmo de Recomendación
- [x] Task: Escribir pruebas unitarias con datos simulados (mocking `ResultadoDiagnostico`) que definan el comportamiento esperado del algoritmo de pesos.
- [x] Task: Implementar la función `calcular_recomendacion` que procese los resultados y aplique la lógica de ponderación por tema.
- [x] Task: Implementar la lógica de resolución de empates (seleccionar el primer tema encontrado).
- [x] Task: Verificar que la función devuelve la estructura detallada (ID, nombre, métrica).
- [x] Task: Ejecutar pruebas y verificar cobertura >80% para el nuevo servicio.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Lógica del Algoritmo de Recomendación' (Protocol in workflow.md)

## Phase 3: Integración y Limpieza
- [x] Task: Refactorizar si es necesario para asegurar que el código sea idiomático y siga las guías de estilo del proyecto.
- [x] Task: Asegurar que todos los métodos públicos del servicio estén documentados con docstrings.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Integración y Limpieza' (Protocol in workflow.md)
