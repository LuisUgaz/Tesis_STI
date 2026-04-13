# Implementation Plan - HU25 - Visualizar insignias obtenidas

Este plan detalla la mejora de la interfaz de logros para permitir una consulta detallada de las insignias ganadas por el estudiante.

## Fase 1: Enriquecimiento de Datos (Backend)
- [x] **Tarea: Optimizar Consulta de Logros en la Vista**
    - [x] Modificar `ProfileView` en `AppGestionUsuario/views.py` para obtener los objetos `LogroEstudiante` completos (incluyendo fecha).
    - [x] Implementar lÃ³gica de ordenamiento: ganadas (recientes primero) seguidas de bloqueadas.
- [ ] **Tarea: Conductor - User Manual Verification 'Fase 1: Enriquecimiento de Datos' (Protocol in workflow.md)**

## Fase 2: Interfaz de Usuario y Modal (Frontend)
- [x] **Tarea: Implementar Modal de Detalle de Insignia**
    - [x] Crear estructura HTML oculta para el modal en `profile.html`.
    - [x] AÃ±adir estilos CSS para el modal y el efecto de escala de grises en insignias bloqueadas.
    - [x] Escribir JavaScript para manejar la apertura del modal con los datos de la insignia seleccionada.
- [ ] **Tarea: Conductor - User Manual Verification 'Fase 2: Interfaz de Usuario' (Protocol in workflow.md)**

## Fase 3: ValidaciÃ³n y Pulido
- [x] **Tarea: VerificaciÃ³n de Seguridad y Privacidad**
    - [x] Asegurar que los datos de obtenciÃ³n mostrados correspondan exclusivamente al usuario autenticado.
- [x] **Tarea: VerificaciÃ³n Final y Cobertura**
    - [x] Ejecutar pruebas de visualizaciÃ³n y asegurar >80% de cobertura en la lÃ³gica de la vista.
- [ ] **Tarea: Conductor - User Manual Verification 'Fase 3: ValidaciÃ³n y Pulido' (Protocol in workflow.md)**
