# Plan de Implementación - HU43: Visualización de Teoría mediante Carrusel

## Fase 1: Actualización del Backend y Modelo de Datos
- [x] **Task: Refinar Modelo de Datos para Progreso**
    - [x] Añadir campo `porcentaje_completado` al modelo `ProgresoEstudiante` en `AppTutoria/models.py`.
    - [x] Ejecutar migraciones (`makemigrations` y `migrate`).
- [x] **Task: Actualizar Servicio de Registro de Progreso**
    - [x] Modificar `registrar_progreso` en `AppTutoria/services.py` para soportar actualizaciones incrementales en el tipo 'Teoría'.
    - [x] Implementar lógica: Si ya existe un registro de 'Teoría' para el tema/usuario, actualizar el `referencia_id` (página) y `porcentaje_completado`.
- [x] **Task: Crear Vista API para Actualización de Progreso**
    - [x] Crear la vista `actualizar_progreso_teoria` en `AppTutoria/views.py` para recibir peticiones AJAX.
    - [x] Registrar la ruta en `AppTutoria/urls.py`.

## Fase 2: Implementación del Carrusel en la Interfaz
- [x] **Task: Estructura y Estilos del Carrusel**
    - [x] Modificar `AppTutoria/templates/AppTutoria/tema_detalle.html` para incluir el contenedor del carrusel.
    - [x] Crear los estilos CSS para el visor, botones de navegación e indicador de progreso.
    - [x] Implementar el estilo "Lightbox" para la vista de pantalla completa.
- [x] **Task: Lógica del Carrusel con Vanilla JS**
    - [x] Implementar navegación "Anterior" y "Siguiente".
    - [x] Actualizar dinámicamente el indicador "Página X de Y".
    - [x] Implementar soporte para flechas del teclado.
    - [x] Implementar funcionalidad de Zoom básico en la imagen.
- [x] **Task: Integración AJAX de Progreso**
    - [x] Implementar llamada asíncrona que notifique al servidor cuando el estudiante avanza a una nueva imagen.
    - [x] Asegurar que el porcentaje se actualice correctamente en la base de datos.

## Fase 3: Pruebas y Validación Final
- [x] **Task: Pruebas de Integridad y Casos Borde**
    - [x] Verificar comportamiento cuando el tema no tiene imágenes (mensaje de advertencia).
    - [x] Validar que el botón de PDF original siga funcionando correctamente como complemento.
    - [x] Realizar pruebas de responsividad para asegurar que el carrusel funcione en móviles.
- [x] **Task: Conductor - User Manual Verification 'Visualización de Teoría mediante Carrusel' (Protocol in workflow.md)**
