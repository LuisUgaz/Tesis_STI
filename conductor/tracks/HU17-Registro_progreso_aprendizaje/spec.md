# Specification: HU17 - Registro de progreso de aprendizaje

## Overview
Implementar un sistema de persistencia centralizado para registrar el progreso de los estudiantes en diversas actividades educativas (ejercicios, videos, teoría y exámenes) dentro de la plataforma. Este registro servirá como evidencia histórica del avance del estudiante por cada tema.

## Functional Requirements
1. **Modelo de Progreso Centralizado**: Crear un modelo `ProgresoEstudiante` en la aplicación `AppTutoria`.
2. **Atributos Obligatorios**:
    - **Estudiante**: Referencia al usuario.
    - **Tema**: Referencia al tema de estudio.
    - **Tipo de Actividad**: Identificador del tipo de actividad realizada (Ejercicio, Video, Teoría, Examen).
    - **Fecha**: Fecha y hora del registro.
    - **Grado y Sección**: Almacenar el grado y la sección del estudiante al momento de realizar la actividad (capturados de su perfil).
    - **Referencia a la Actividad**: ID de la actividad específica realizada (opcional/genérico).
3. **Persistencia Automática**: El sistema debe generar un registro de progreso cada vez que un estudiante completa una actividad.
    - Al resolver un ejercicio.
    - Al visualizar un video.
    - Al leer el contenido teórico de un tema.
    - Al finalizar un examen de diagnóstico.
4. **Historial Completo**: Permitir múltiples registros para el mismo tema y estudiante, manteniendo un historial de todos los intentos o interacciones.

## Non-Functional Requirements
- **Consistencia**: Asegurar la integridad referencial con los modelos de `User` y `Tema`.
- **Escalabilidad**: El modelo debe ser capaz de crecer sin afectar el rendimiento de las consultas de visualización (aunque estas están fuera de alcance ahora).

## Acceptance Criteria
- [ ] Existe un modelo `ProgresoEstudiante` en `AppTutoria/models.py`.
- [ ] El modelo incluye campos para usuario, tema, tipo de actividad, fecha, grado y sección.
- [ ] Al completar un ejercicio, se guarda automáticamente un registro en `ProgresoEstudiante`.
- [ ] Al ver un video o leer teoría, se guarda automáticamente un registro en `ProgresoEstudiante`.
- [ ] Al finalizar un examen, se guarda automáticamente un registro en `ProgresoEstudiante`.
- [ ] El registro incluye los datos de grado y sección vigentes en el perfil del usuario.

## Out of Scope
- Visualización del historial de progreso.
- Métricas agregadas o promedios de desempeño.
- Reportes para docentes.
