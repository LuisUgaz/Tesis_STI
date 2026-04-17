# Track Specification - HU23 - Subida de nivel

## Overview
Esta funcionalidad permite a los estudiantes visualizar su crecimiento acadÃ©mico mediante un sistema de niveles. Al acumular puntos de experiencia (XP), el sistema recalcula automÃ¡ticamente el nivel del estudiante basado en umbrales fijos, persistiendo este valor y notificando visualmente el cambio para mantener la motivaciÃ³n.

## Functional Requirements
- **Regla de Niveles Fija:** ImplementaciÃ³n de una fÃ³rmula de niveles basada en incrementos fijos de 100 puntos (Nivel 1: 0-99, Nivel 2: 100-199, etc.).
- **Persistencia en Profile:** ActualizaciÃ³n del campo `nivel_estudiante` en el modelo `Profile` en `AppGestionUsuario/models.py`.
- **Motor de Subida de Nivel:** IntegraciÃ³n con el `GamificationService` para verificar cambios de nivel tras cada asignaciÃ³n de puntos.
- **Feedback Visual (Toast):** 
  - NotificaciÃ³n flotante especial (Toast) de color distintivo al subir de nivel.
  - Mensaje: "Â¡Felicidades! Has alcanzado el Nivel X".
- **VisualizaciÃ³n en UI:**
  - Mostrar el nivel actual en la cabecera de las vistas de prÃ¡ctica junto a los puntos XP.
  - Mostrar el nivel en el perfil del estudiante con un distintivo visual.

## Technical Constraints
- El campo `nivel_estudiante` debe ser un entero positivo (PositiveIntegerField) con valor inicial de 1.
- La lÃ³gica de subida de nivel debe ser centralizada en el servicio de gamificaciÃ³n.
- La notificaciÃ³n debe ser asÃ­ncrona (AJAX) tras la validaciÃ³n de respuestas.

## Acceptance Criteria
- El nivel aumenta automÃ¡ticamente al alcanzar cada umbral de 100 puntos.
- El nivel no sube antes de alcanzar el umbral necesario.
- El valor del nivel se guarda correctamente en la base de datos (modelo Profile).
- Se muestra una notificaciÃ³n Toast al subir de nivel en la prÃ¡ctica.
- El nivel es visible en la cabecera de prÃ¡cticas y en el perfil.

## Out of Scope
- Sistema de insignias o medallas por nivel.
- Ranking de niveles entre estudiantes (Leaderboards).
- Desbloqueo de contenido bloqueado por nivel.
