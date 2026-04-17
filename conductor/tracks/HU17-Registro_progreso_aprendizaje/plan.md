# Plan de Implementación: HU17 - Registro de progreso de aprendizaje

Este plan detalla los pasos para implementar un sistema de registro de progreso centralizado en `AppTutoria`, integrándolo con las actividades de ejercicios, videos, teoría y exámenes.

## Fase 1: Base de Datos y Modelo Centralizado [checkpoint: completado]
- [x] Task: Crear el modelo `ProgresoEstudiante` en `AppTutoria/models.py`. (f47892a)
    - [x] Definir campos: `usuario`, `tema`, `tipo_actividad`, `fecha_registro`, `grado`, `seccion`, `referencia_id`.
    - [x] Ejecutar migraciones: `python manage.py makemigrations AppTutoria` y `python manage.py migrate`.
- [x] Task: Crear un servicio/utilidad para registrar progreso. (a2b1c3d)
    - [x] Implementar `registrar_progreso(usuario, tema, tipo_actividad, referencia_id=None)` en `AppTutoria/services.py`.
    - [x] La función debe extraer automáticamente `grado` y `seccion` del perfil del usuario.
- [x] Task: Pruebas unitarias para el modelo y servicio. (e5f6g7h)
    - [x] Escribir pruebas que verifiquen la creación correcta de registros y la captura de grado/sección.
- [x] Task: Conductor - User Manual Verification 'Fase 1' (Protocol in workflow.md)

## Fase 2: Integración con Ejercicios (AppEvaluar) [checkpoint: completado]
- [x] Task: Escribir pruebas de integración para el registro tras completar un ejercicio.
- [x] Task: Modificar la vista de resolución de ejercicios en `AppEvaluar/views.py` para llamar a `registrar_progreso`.
- [x] Task: Verificar que al finalizar un ejercicio se cree el registro correspondiente.
- [x] Task: Conductor - User Manual Verification 'Fase 2' (Protocol in workflow.md)

## Fase 3: Integración con Videos y Teoría (AppTutoria) [checkpoint: completado]
- [x] Task: Escribir pruebas de integración para el registro tras ver un video o leer teoría.
- [x] Task: Modificar la vista de detalle de tema (teoría) para registrar progreso.
- [x] Task: Modificar la lógica de visualización de videos para registrar progreso.
- [x] Task: Conductor - User Manual Verification 'Fase 3' (Protocol in workflow.md)

## Fase 4: Integración con Exámenes (AppEvaluar) [checkpoint: completado]
- [x] Task: Escribir pruebas de integración para el registro tras finalizar un examen.
- [x] Task: Modificar la vista de resultados de examen en `AppEvaluar/views.py` para registrar progreso.
- [x] Task: Verificar que al finalizar un examen de diagnóstico se cree el registro correspondiente.
- [x] Task: Conductor - User Manual Verification 'Fase 4' (Protocol in workflow.md)

---
**Nota:** Siguiendo las instrucciones del usuario, no se realizarán commits automáticos. La verificación será manual y mediante pruebas automatizadas.
