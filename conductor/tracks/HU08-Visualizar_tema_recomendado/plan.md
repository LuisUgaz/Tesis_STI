# Implementation Plan: HU08 - Visualizar tema recomendado

## Phase 1: Modelo y Persistencia de la Recomendación
- [x] Task: Crear el modelo `RecomendacionEstudiante` en `AppEvaluar` para persistir el tema recomendado.
    - [x] Definir campos: `usuario` (FK a User), `tema` (CharField), `fecha_generacion`, `metrica_desempeno`.
- [x] Task: Actualizar el servicio de recomendación (`services.py`) para que guarde el resultado en el nuevo modelo después del diagnóstico.
- [x] Task: Escribir pruebas unitarias (TDD) para verificar la persistencia y recuperación de la recomendación.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Modelo y Persistencia de la Recomendación' (Protocol in workflow.md)

## Phase 2: Vista de Lista de Temas
- [x] Task: Crear la vista `lista_temas` en `AppTutoria/views.py`.
    - [x] Definir la lista de temas (Triángulos, Ángulos, Segmentos, Rectas, Geometría Plana).
    - [x] Obtener la recomendación del estudiante desde la BD.
    - [x] Reordenar la lista para colocar el recomendado al principio.
- [x] Task: Configurar las URLs para `AppTutoria` y enlazarla desde el dashboard/home.
- [x] Task: Escribir pruebas para la vista asegurando que el contexto incluya la recomendación y se maneje el estado de "Sin Recomendación".
- [x] Task: Conductor - User Manual Verification 'Phase 2: Vista de Lista de Temas' (Protocol in workflow.md)

## Phase 3: Interfaz de Usuario y Estilos
- [x] Task: Crear el template `AppTutoria/lista_temas.html`.
- [x] Task: Implementar el diseño visual con Badges para el tema recomendado.
- [x] Task: Añadir el mensaje informativo/invitación para estudiantes sin diagnóstico.
- [x] Task: Aplicar estilos CSS (utilizando el estilo del proyecto).
- [x] Task: Conductor - User Manual Verification 'Phase 3: Interfaz de Usuario y Estilos' (Protocol in workflow.md)
