# Specification: HU06 - Registrar resultado diagnóstico

## Overview
Implementar la persistencia de los resultados del examen diagnóstico para el Sistema Tutor Inteligente Adaptativo. Esta funcionalidad permitirá que el sistema almacene el desempeño inicial del estudiante para su uso en procesos posteriores de tutoría y adaptación.

## Functional Requirements
1. **Modelo de Datos:**
   - Crear el modelo `ResultadoDiagnostico` en la aplicación `AppEvaluar`.
   - Atributos requeridos: `estudiante` (FK a User), `puntaje` (Decimal), `fecha_realizacion` (DateTimeField, auto_now_add=True).
2. **Procesamiento de Respuestas:**
   - La vista debe recibir un POST con `examen_id` y pares `pregunta_<id>=<respuesta_id>`.
   - Validar cada respuesta seleccionada contra la respuesta correcta definida en el modelo de Pregunta/Respuesta.
3. **Cálculo de Calificación:**
   - Algoritmo: `(Respuestas Correctas / Total de Preguntas) * 100`.
   - El resultado debe ser un valor numérico almacenado en el modelo.
4. **Control de Intentos:**
   - Implementar un bloqueo para que cada estudiante solo pueda registrar **un único resultado** de diagnóstico.
   - Si un estudiante ya tiene un registro en `ResultadoDiagnostico`, se debe impedir un nuevo envío.
5. **Persistencia:**
   - Los datos deben guardarse correctamente en la base de datos PostgreSQL.

## Non-Functional Requirements
- **Consistencia:** Seguir las convenciones de Django y la estructura actual del proyecto.
- **Idioma:** Toda la lógica interna, mensajes y documentación deben estar en español.
- **Seguridad:** Asegurar que el resultado se asocie correctamente al usuario autenticado.

## Acceptance Criteria
- [ ] El sistema calcula correctamente el puntaje basado en las respuestas enviadas.
- [ ] El resultado (puntaje, fecha y usuario) se guarda correctamente en la base de datos.
- [ ] Un estudiante no puede realizar el examen diagnóstico más de una vez.
- [ ] Los datos persistidos en PostgreSQL coinciden con lo procesado por el backend.

## Out of Scope
- Generación de recomendaciones automáticas.
- Visualización de rankings o reportes detallados.
- Historial avanzado de intentos.
