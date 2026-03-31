# Specification: HU07 - Procesar resultados para recomendación

## Overview
Esta historia de usuario se centra en el desarrollo de la lógica de negocio necesaria para procesar los resultados obtenidos en el examen diagnóstico de un estudiante. El objetivo es determinar de manera automática cuál es el tema geométrico que presenta mayor dificultad para el alumno y, por ende, el que debe ser reforzado prioritariamente.

## Functional Requirements
1.  **Carga de Resultados:** El sistema debe ser capaz de obtener los datos de `ResultadoDiagnostico` para el estudiante actual.
2.  **Algoritmo de Recomendación (Pesos por Tema):**
    - Se debe calcular un puntaje de necesidad por tema.
    - Se aplicará una lógica de ponderación para identificar el tema con menor desempeño.
3.  **Gestión de Empates:** En caso de que dos o más temas tengan el mismo nivel de necesidad, el sistema seleccionará el primero que encuentre en la lista procesada.
4.  **Generación de Salida Detallada:** El servicio debe devolver un objeto o diccionario que incluya:
    - Identificador del tema.
    - Nombre del tema.
    - Métrica o puntaje que justificó la recomendación.
5.  **Validación de Datos:** Si no existen resultados previos para el estudiante, el sistema debe lanzar una excepción controlada para evitar cálculos erróneos.

## Non-Functional Requirements
1.  **Encapsulamiento:** La lógica debe residir en un servicio o módulo independiente dentro de `AppEvaluar` para facilitar su reutilización y evolución.
2.  **Evolución:** El diseño debe permitir la integración futura de algoritmos más complejos (IA, lógica difusa, etc.) sin afectar drásticamente el flujo actual.
3.  **Consistencia:** Uso estricto de Django y PostgreSQL para las consultas y el manejo de modelos.

## Acceptance Criteria
- **Escenario: Procesamiento exitoso del diagnóstico**
    - **Given** que existen resultados del examen diagnóstico del estudiante.
    - **When** el sistema ejecuta el algoritmo de recomendación.
    - **Then** debe calcular el tema con mayor necesidad de refuerzo.
    - **And** debe generar una recomendación detallada sin errores.
- **Escenario: Manejo de ausencia de datos**
    - **Given** que un estudiante no ha rendido el examen diagnóstico.
    - **When** se intenta procesar la recomendación.
    - **Then** el sistema debe lanzar una excepción controlada.

## Out of Scope
- Visualización de la recomendación en la interfaz de usuario (templates).
- Asignación automática de ejercicios o rutas de aprendizaje.
- Generación de múltiples recomendaciones simultáneas.
