# Plan de Implementación: HU12 - Visualización de Videos Recomendados

## Fase 1: Base de Datos y Modelado
- [x] Task: Crear el modelo `VideoTema` en `AppTutoria/models.py`.
- [x] Task: Registrar el modelo `VideoTema` en `AppTutoria/admin.py` para permitir la gestión desde el panel administrativo.
- [x] Task: Generar y aplicar las migraciones correspondientes.
- [x] Task: Conductor - User Manual Verification 'Fase 1: Base de Datos y Modelado' (Protocol in workflow.md)

## Fase 2: Lógica del Backend (Vistas y URLs)
- [x] Task: Implementar la vista `video_list` en `AppTutoria/views.py`. Esta vista debe filtrar los videos por el `slug` del tema y verificar los permisos del estudiante.
- [x] Task: Configurar la URL para la lista de videos en `AppTutoria/urls.py`.
- [x] Task: Escribir pruebas unitarias para la vista `video_list` (acceso, filtrado por tema, permisos).
- [x] Task: Conductor - User Manual Verification 'Fase 2: Lógica del Backend' (Protocol in workflow.md)

## Fase 3: Interfaz de Usuario (Frontend)
- [x] Task: Crear el template `AppTutoria/videos.html` con una grilla de tarjetas moderna (CSS Grid/Flexbox).
- [x] Task: Implementar la visualización del video (tag `<video>` o reproductor básico).
- [x] Task: Actualizar el sidebar en `AppTutoria/templates/AppTutoria/tema_detalle.html` para habilitar y enlazar a la nueva vista de videos.
- [x] Task: Conductor - User Manual Verification 'Fase 3: Interfaz de Usuario' (Protocol in workflow.md)

## Fase 4: Integración y Pruebas Finales
- [x] Task: Realizar pruebas de integración para asegurar que el flujo Estudiante -> Tema -> Video funciona correctamente.
- [x] Task: Validar que el diseño sea responsive en diferentes tamaños de pantalla.
- [x] Task: Conductor - User Manual Verification 'Fase 4: Integración y Pruebas Finales' (Protocol in workflow.md)
