# Track Specification - HU22 - AsignaciÃ³n de puntos por actividad

## Overview
Esta funcionalidad implementa el nÃºcleo del sistema de gamificaciÃ³n del STI, permitiendo a los estudiantes acumular puntos de experiencia por sus interacciones educativas. El objetivo es incentivar la perseverancia y el dominio de los temas de geometrÃ­a mediante una recompensa visual y cuantificable.

## Functional Requirements
- **Regla Centralizada de Puntos:** ImplementaciÃ³n de una lÃ³gica de cÃ¡lculo basada en el tipo de actividad, el resultado y la dificultad:
  - **Ejercicios:** Puntos por acierto diferenciados por nivel (BÃ¡sico: 10, Intermedio: 20, Avanzado: 30). Intentos fallidos otorgan un puntaje mÃ­nimo por esfuerzo (ej. 2 pts).
  - **Videos:** Puntos fijos por visualizaciÃ³n completa (ej. 5 pts).
  - **TeorÃ­a:** Puntos fijos por lectura finalizada del material (ej. 5 pts).
- **Persistencia en Perfil:** ActualizaciÃ³n del campo `puntos_acumulados` en el modelo `Profile` de cada estudiante.
- **Feedback Visual Inmediato:** 
  - NotificaciÃ³n flotante (Toast) al ganar puntos.
  - AnimaciÃ³n de "+X pts" en la vista de resoluciÃ³n de ejercicios.
- **Trazabilidad:** IntegraciÃ³n con los servicios de registro de progreso (`HU17`) para asegurar que los puntos se asignen solo una vez por actividad (evitar duplicados en videos/teorÃ­a).

## Technical Constraints
- El campo `puntos_acumulados` debe ser un entero positivo en el modelo `Profile`.
- La asignaciÃ³n de puntos debe ser atÃ³mica para garantizar la consistencia en caso de errores de red.
- La lÃ³gica de puntos debe residir en un servicio centralizado para facilitar futuros ajustes de balanceo.

## Acceptance Criteria
- Se asignan puntos correctamente tras validar un ejercicio (segÃºn acierto y nivel).
- Se asignan puntos al completar la visualizaciÃ³n de un video recomendado.
- Se asignan puntos al finalizar la lectura de un marco teÃ³rico.
- El total de puntos en el perfil se actualiza correctamente.
- Aparece una notificaciÃ³n visual tras cada asignaciÃ³n exitosa.

## Out of Scope
- Sistema de niveles (LVL).
- Desbloqueo de insignias o medallas.
- Tablas de clasificaciÃ³n (Leaderboards).
- Historial detallado de transacciones de puntos (solo se guarda el acumulado).
