# Track Specification - HU24 - Asignación automática de insignias

## Overview
Esta funcionalidad introduce un sistema de logros visuales (insignias) para incentivar la participación y el dominio académico. El sistema evaluará automáticamente el progreso del estudiante tras cada actividad relevante y otorgará insignias basadas en reglas predefinidas, las cuales serán visibles en una galería dentro del perfil del usuario.

## Functional Requirements
- **Sistema de Modelos de Insignias:**
  - Modelo `Insignia`: Almacena metadatos como nombre, descripción técnica, icono (URL o clase CSS) y tipo de regla.
  - Modelo `LogroEstudiante`: Registra la relación entre un estudiante y las insignias obtenidas, incluyendo la fecha de obtención.
- **Motor de Reglas Automático:** Integración con `GamificationService` para evaluar:
  - **Hitos:** Primera actividad completada.
  - **Dominio:** Precisión > 80% tras completar un set de ejercicios de un tema.
  - **Constancia:** Completar actividades en 3 días diferentes (simulado o real).
  - **Progresión:** Alcanzar niveles específicos (Nivel 5, 10).
- **Notificaciones Asíncronas:** Mostrar un Toast especial ("¡Nueva Insignia Ganada!") en el frontend tras la validación de una actividad.
- **Galería de Logros:** Sección visual en `profile.html` que muestre los iconos de las insignias obtenidas (y opcionalmente las no obtenidas en gris).

## Technical Constraints
- Las insignias deben otorgarse **una sola vez** por estudiante (evitar duplicados).
- La evaluación de reglas debe ocurrir después de la actualización de métricas y puntos.
- Se debe utilizar el sistema de persistencia de Django para asegurar integridad referencial.

## Acceptance Criteria
- El estudiante recibe la insignia "Primeros Pasos" al completar su primer ejercicio.
- Las insignias se guardan correctamente en la base de datos vinculadas al usuario.
- El estudiante visualiza sus insignias en el perfil en una cuadrícula organizada.
- Se muestra un Toast en tiempo real al ganar un logro.

## Out of Scope
- Interfaz de administración para crear nuevas insignias (se cargarán mediante fixtures o migraciones de datos en esta fase).
- Compartir insignias en redes sociales.
