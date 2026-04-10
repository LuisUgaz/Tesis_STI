# Plan de ImplementaciÃ³n: HU13 - Registrar visualizaciÃ³n de videos

## Fase 1: Base de Datos y Modelado
- [x] Task: Crear el modelo `VisualizacionVideo` en `AppTutoria/models.py`.
- [x] Task: Registrar el modelo `VisualizacionVideo` en `AppTutoria/admin.py` con columnas personalizadas (Grado, SecciÃ³n, Video, Contador, Ãšltima VisualizaciÃ³n).
- [x] Task: Generar y aplicar las migraciones correspondientes.
- [x] Task: Conductor - User Manual Verification 'Fase 1: Base de Datos y Modelado' (Protocol in workflow.md)

## Fase 2: LÃ³gica del Backend (Endpoint AJAX)
- [x] Task: Implementar la vista `registrar_visualizacion` en `AppTutoria/views.py`. Esta vista debe recibir el ID del video por POST, verificar autenticaciÃ³n y permiso (tema recomendado), y actualizar o crear el registro en la base de datos.
- [x] Task: Configurar la URL para el endpoint en `AppTutoria/urls.py`.
- [x] Task: Escribir pruebas unitarias para el registro de visualizaciÃ³n (creaciÃ³n, incremento de contador, permisos).
- [~] Task: Conductor - User Manual Verification 'Fase 2: LÃ³gica del Backend' (Protocol in workflow.md)

## Fase 3: IntegraciÃ³n con el Frontend (Disparador JS)
- [x] Task: Actualizar el script en `AppTutoria/templates/AppTutoria/videos.html` para capturar el evento `ended` del elemento `<video>`.
- [x] Task: Implementar la llamada asÃ­ncrona (Fetch API) al endpoint `registrar_visualizacion` al finalizar el video.
- [x] Task: Conductor - User Manual Verification 'Fase 3: IntegraciÃ³n con el Frontend' (Protocol in workflow.md)

## Fase 4: ValidaciÃ³n Final y Reporte Admin
- [x] Task: Realizar pruebas de integración para asegurar que el flujo Estudiante -> Ver Video -> Registro en Admin funciona correctamente.
- [x] Task: Verificar que el reporte administrativo muestra correctamente el grado y la secciÃ³n del estudiante obtenidos de su perfil.
- [x] Task: Conductor - User Manual Verification 'Fase 4: ValidaciÃ³n Final y Reporte Admin' (Protocol in workflow.md)
