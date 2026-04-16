# Specification (HU41): Asignar exámenes a temas

## Overview
Esta historia de usuario permite a los docentes vincular los exámenes que han creado con temas específicos del sistema. Esto asegura que el material de evaluación esté organizado y sea fácilmente accesible para los estudiantes desde el contexto del tema que están estudiando.

## Functional Requirements
- **FR-01: Interfaz de Asignación**: El docente podrá asignar un examen a un tema a través de la interfaz de edición (UpdateView) del examen en `AppEvaluar`.
- **FR-02: Modelo de Datos**: La relación entre `Examen` y `Tema` será de 1:N (muchos exámenes pueden pertenecer a un mismo tema, pero un examen es único para un tema).
- **FR-03: Visualización para Estudiantes**: Los estudiantes verán los exámenes disponibles dentro de la vista de detalle del tema (`tema_detalle` en `AppTutoria`).
- **FR-04: Gestión de Eliminación**: Al eliminar un examen (como se definió en la HU39), las preguntas asociadas deben quedar libres para ser reutilizadas en nuevos exámenes.
- **FR-05: Restricción de Acceso**: La gestión de asignación es exclusiva para el rol de 'Docente'.

## Acceptance Criteria
- **Scenario: Asignación exitosa**
  - Dado un docente en el formulario de edición de un examen.
  - Cuando selecciona un tema disponible y guarda.
  - Entonces el sistema guarda la relación y el examen aparece en la vista de detalle de ese tema para los estudiantes.
- **Scenario: Visualización en el tema**
  - Dado un estudiante que consulta el detalle de un tema.
  - Cuando el tema tiene exámenes asignados.
  - Entonces el sistema muestra una sección de "Exámenes de Evaluación" con enlaces a cada uno.
- **Scenario: Regla de Unicidad**
  - Dado que los exámenes son únicos por tema.
  - Cuando un examen ya está asignado, no puede estar presente en otro tema simultáneamente.

## Out of Scope
- Resolución del examen por el estudiante (HU futura).
- Calificación automática.
- Gestión avanzada de intentos.
