# Plan de Implementación: HU32 - Clasificar Preguntas por Tema y Nivel

## Fase 1: Alineación de Modelos y Migración de Datos
- [x] Task: Crear pruebas unitarias para validar la nueva estructura de `Pregunta`.
    - [x] Escribir tests que verifiquen la obligatoriedad de `tema` (FK) y `dificultad` en `Pregunta`.
    - [x] Ejecutar y confirmar fallo (Fase Roja).
- [x] Task: Actualizar el modelo `Pregunta` en `AppEvaluar/models.py`.
    - [x] Cambiar `categoria` (CharField) por `tema` (ForeignKey a `AppTutoria.Tema`).
    - [x] Añadir campo `dificultad` con las mismas opciones que `Ejercicio`.
- [x] Task: Crear y ejecutar migraciones de datos seguras.
    - [x] Implementar migración intermedia para mapear valores de `categoria` (texto) a IDs de `Tema`.
    - [x] Ejecutar `makemigrations` y `migrate`.
- [x] Task: Confirmar que las pruebas de modelo pasan (Fase Verde).
- [x] Task: Conductor - User Manual Verification 'Alineación de Modelos' (Protocolo en workflow.md)

## Fase 2: Lógica de Filtrado y Búsqueda (Backend)
- [x] Task: Crear pruebas para el filtrado en `BancoPreguntasListView`.
    - [x] Test de filtrado por tema vía URL param.
    - [x] Test de filtrado por dificultad vía URL param.
    - [x] Ejecutar y confirmar fallo (Fase Roja).
- [x] Task: Refactorizar `BancoPreguntasListView` en `AppEvaluar/views.py`.
    - [x] Sobrescribir `get_queryset` para capturar parámetros GET y aplicar filtros de Django.
- [x] Task: Confirmar que las pruebas de filtrado pasan (Fase Verde).
- [x] Task: Conductor - User Manual Verification 'Lógica de Filtrado' (Protocolo en workflow.md)

## Fase 3: Interfaz de Usuario Avanzada (Frontend)
- [x] Task: Implementar barra de filtros en el listado del banco.
    - [x] Actualizar `banco_preguntas_list.html` con selectores para Tema y Dificultad.
    - [x] Asegurar que los filtros se mantengan (sticky) tras la búsqueda.
- [x] Task: Actualizar formularios de creación/edición de Diagnóstico.
    - [x] Validar que `tema` y `dificultad` sean campos destacados.
- [x] Task: Conductor - User Manual Verification 'Interfaz de Usuario' (Protocolo en workflow.md)

## Fase 4: Validación de Integridad Histórica
- [x] Task: Verificación final de consistencia.
    - [x] Validar que los resultados de exámenes previos sigan vinculados correctamente tras el cambio de `Pregunta.categoria` a `Pregunta.tema`.
- [x] Task: Conductor - User Manual Verification 'Validación de Integridad' (Protocolo en workflow.md)
