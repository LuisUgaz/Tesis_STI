# Plan de Implementación: HU09 - Visualizar Temas Disponibles

Este plan sigue la metodología TDD (Desarrollo Dirigido por Pruebas) y el flujo de trabajo definido en `workflow.md`.

## Fase 1: Persistencia de Datos (Modelo Tema)
- [x] Task: Definir y crear el modelo `Tema` en `AppTutoria/models.py`.
    - [ ] Escribir pruebas unitarias para el modelo `Tema` en `AppTutoria/tests_models.py`.
    - [ ] Implementar el modelo `Tema` con campos `nombre` y `descripcion`.
    - [ ] Crear y ejecutar las migraciones necesarias.
- [ ] Task: Conductor - User Manual Verification 'Persistencia de Datos (Modelo Tema)' (Protocol in workflow.md)

## Fase 2: Control de Acceso y Lógica de Vista
- [x] Task: Implementar validación de rol de Estudiante.
    - [x] Escribir pruebas para verificar que solo usuarios con rol 'Estudiante' accedan a la lista.
    - [x] Implementar un decorador o validación en `AppTutoria/views.py` para restringir el acceso.
- [x] Task: Actualizar la vista `lista_temas` para usar la base de datos.
    - [x] Escribir pruebas para asegurar que la vista recupera los temas del modelo `Tema`.
    - [x] Modificar `AppTutoria/views.py` para obtener temas de la BD y mantener la lógica de recomendación.
- [ ] Task: Conductor - User Manual Verification 'Control de Acceso y Lógica de Vista' (Protocol in workflow.md)

## Fase 3: Interfaz de Usuario y Integración
- [x] Task: Adaptar la plantilla `AppTutoria/templates/AppTutoria/lista_temas.html`.
    - [x] Actualizar la plantilla para iterar sobre los objetos `Tema` de la base de datos.
    - [x] Verificar visualmente que el resaltado de recomendaciones siga funcionando correctamente.
- [ ] Task: Conductor - User Manual Verification 'Interfaz de Usuario y Validación Final' (Protocol in workflow.md)

---

**Nota:** No se realizarán commits automáticos. La documentación y comentarios estarán en español.