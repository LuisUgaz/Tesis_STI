# Implementation Plan - HU21 - Visualizar mÃ©tricas de desempeÃ±o

Este plan detalla la creaciÃ³n de la interfaz visual para que el estudiante consulte sus mÃ©tricas acadÃ©micas personalizadas.

## Fase 1: Backend y Rutas
- [x] **Tarea: Definir URL y Vista de Dashboard** [manual]
    - [x] Registrar la ruta `/usuarios/mi-progreso/` en `AppGestionUsuario/urls.py`.
    - [x] Crear la vista `MiProgresoView` en `AppGestionUsuario/views.py` (LoginRequired + StudentRequired).
    - [x] Implementar la lÃ³gica para recuperar el objeto `MetricasEstudiante` del usuario actual.
- [x] **Tarea: Escribir Pruebas de Acceso y Datos** [manual]
    - [x] Probar que solo estudiantes autenticados acceden a la vista.
    - [x] Verificar que la vista entrega los datos correctos al contexto (mÃ©tricas globales y por tema).
- [x] **Tarea: Conductor - User Manual Verification 'Fase 1: Backend y Rutas' (Protocol in workflow.md)** [manual]

## Fase 2: Frontend y Plantilla
- [x] **Tarea: Crear Plantilla `mi_progreso.html`** [manual]
    - [x] DiseÃ±ar el layout con tarjetas de resumen (PrecisiÃ³n, Rendimiento, Tiempo).
    - [x] Implementar el listado de temas con barras de progreso utilizando los datos de `dominio_por_tema`.
    - [x] Aplicar estilos CSS coherentes con la lÃ­nea visual gamificada del proyecto.
- [x] **Tarea: LÃ³gica de "Estado VacÃ­o"** [manual]
    - [x] AÃ±adir condicionales en la plantilla para mostrar mensaje de "Sin actividades" si no existen mÃ©tricas.
- [x] **Tarea: Conductor - User Manual Verification 'Fase 2: Frontend y Plantilla' (Protocol in workflow.md)** [manual]

## Fase 3: IntegraciÃ³n y NavegaciÃ³n
- [x] **Tarea: Actualizar MenÃº de NavegaciÃ³n** [manual]
    - [x] Modificar `templates/home.html` (o el componente de navegaciÃ³n base) para incluir el enlace "Mi progreso".
    - [x] Asegurar que el enlace solo sea visible para el rol 'Estudiante'.
- [x] **Tarea: VerificaciÃ³n Final** [manual]
    - [x] Realizar pruebas de integraciÃ³n navegando desde el inicio hasta el panel de progreso.
    - [x] Validar visualizaciÃ³n en diferentes tamaÃ±os de pantalla (Responsive).
- [x] **Tarea: Conductor - User Manual Verification 'Fase 3: IntegraciÃ³n y NavegaciÃ³n' (Protocol in workflow.md)** [manual]
