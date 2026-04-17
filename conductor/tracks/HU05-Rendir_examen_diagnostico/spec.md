# Specification: HU05 - Rendir Examen Diagnóstico

## Overview
Implementación de un examen diagnóstico para que el estudiante rinda una evaluación inicial de geometría. El sistema debe capturar las respuestas, calcular el puntaje y almacenar el nivel detectado por tema para futuras recomendaciones.

## Requirements

### Functional
- **Gestión de Preguntas:** Las preguntas se administrarán vía Django Admin.
- **Tipos de Pregunta:** Soporte para "Opción Múltiple" y "Respuesta Corta (Texto)".
- **Restricción de Acceso:** Solo usuarios con rol 'Estudiante' pueden realizar el examen.
- **Temporizador Global:** El examen tendrá un límite de tiempo global (ej. 45 min) controlado por el sistema.
- **Registro de Resultados:** El sistema debe guardar cada respuesta individual y el resultado consolidado (puntaje total y porcentaje por tema).
- **Feedback Post-Envío:** Al finalizar, se mostrará un mensaje de éxito, el puntaje total y un resumen de desempeño por temas.

### Non-Functional
- **Integridad:** Uso de modelos relacionales en PostgreSQL (Django ORM).
- **Usabilidad:** Interfaz clara y motivadora, siguiendo el estilo del proyecto.

## Acceptance Criteria
- **Escenario: Realización del Examen**
  - **Dado** que un estudiante autenticado accede a la sección de examen diagnóstico.
  - **Cuando** responde las preguntas (opción múltiple y texto corto) y las envía antes de que expire el tiempo.
  - **Entonces** el sistema debe validar y registrar todas las respuestas.
  - **Y** debe calcular el puntaje total y el nivel por cada categoría de geometría evaluada.
  - **Y** debe mostrar al estudiante su resultado con un mensaje de éxito.

## Out of Scope
- Algoritmo de recomendación de temas (será parte de una HU posterior).
- Retroalimentación detallada por cada pregunta (explicación de por qué fue correcta/incorrecta).
- Análisis adaptativo complejo durante el examen (las preguntas son fijas para el diagnóstico).
