# Specification: HU39 - Gestionar exámenes por tema

## Descripción General
Esta tarea implementa la funcionalidad para que los docentes gestionen (creen y eliminen) exámenes categorizados por tema, con asignación automática y aleatoria de preguntas disponibles. Estos exámenes son distintos del examen diagnóstico inicial y están destinados a la evaluación continua, el seguimiento del progreso y el ajuste adaptativo de la dificultad dentro del flujo de tutoría.

## Requisitos Funcionales
- **Acceso Restringido:** Solo los usuarios con el rol de docente pueden acceder a este módulo.
- **Modelo Examen:** Crear un nuevo modelo `Examen` en `AppEvaluar`.
    - Campos: `nombre` (Único), `tema` (ForeignKey a `Tema`), `cantidad_preguntas`, `tiempo_limite` (Minutos, Obligatorio), `fecha_creacion`.
- **Gestión de Preguntas:**
    - Se debe modificar el modelo `Pregunta` existente para que el campo `examen` (referencia a `ExamenDiagnostico`) sea opcional (`null=True, blank=True`).
    - Se debe añadir un campo `examen_tema` (ForeignKey opcional al nuevo modelo `Examen`) en el modelo `Pregunta`.
- **Asignación Automática de Preguntas:**
    - Al crear un examen, el sistema debe filtrar las preguntas que:
        1. Pertenezcan al `tema` seleccionado.
        2. **No** estén asociadas a ningún `ExamenDiagnostico` ni a ningún otro `Examen` (es decir, que ambos campos de relación sean nulos).
    - La asignación será aleatoria hasta completar la `cantidad_preguntas` solicitada.
- **Validación de Disponibilidad:**
    - Si el número de preguntas disponibles para el tema es menor a la `cantidad_preguntas`, el examen no se creará y se mostrará un mensaje de error indicando la insuficiencia.
- **Eliminación de Examen:**
    - Al eliminar un examen, las preguntas asociadas deben quedar disponibles nuevamente (se debe limpiar su campo `examen_tema`, no borrar la pregunta).
- **Interfaz del Docente (Dashboard):**
    - Una vista que muestre un resumen de preguntas disponibles por tema.
    - Un formulario para crear un nuevo examen (Nombre, Tema, Cantidad de Preguntas, Tiempo Límite).

## Requisitos No Funcionales
- **Consistencia:** Asegurar que la creación del examen y la asignación de preguntas ocurran de forma atómica.
- **Seguridad:** Validar permisos de docente en todas las vistas y acciones.

## Criterios de Aceptación
- [ ] Los docentes pueden ver un dashboard con el conteo de preguntas disponibles por cada tema.
- [ ] Los docentes pueden crear un examen especificando nombre, tema, cantidad y tiempo límite.
- [ ] El sistema asigna aleatoriamente la cantidad solicitada de preguntas del tema correspondiente.
- [ ] El sistema impide la creación del examen si no hay suficientes preguntas disponibles.
- [ ] Las preguntas asignadas a un examen no pueden asignarse a otro hasta que el primero sea eliminado.
- [ ] Los docentes pueden eliminar un examen, liberando sus preguntas.

## Fuera de Alcance
- Edición de exámenes ya creados (solo registro y eliminación).
- Reasignación manual de preguntas.
- Resolución del examen por parte del estudiante (vista de examen para el alumno).
- Lógica de calificación automática (se abordará en otras tareas).
