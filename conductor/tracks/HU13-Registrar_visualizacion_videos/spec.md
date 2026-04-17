# EspecificaciÃ³n del Track: HU13 - Registrar visualizaciÃ³n de videos

## InformaciÃ³n General
- **ID del Track:** user_track_video_views_20260410
- **DescripciÃ³n:** Implementar el registro y seguimiento de visualizaciones de videos por parte de los estudiantes para llevar un control del uso de recursos educativos.
- **Tipo:** Feature
- **Usuario Principal:** Sistema / Estudiante

## Objetivos
- Registrar cuÃ¡ndo un estudiante termina de ver un video educativo.
- Mantener un contador acumulativo de visualizaciones por relaciÃ³n Usuario-Video.
- Proveer informaciÃ³n sobre el progreso y uso de recursos multimedia a nivel administrativo.

## Requerimientos Funcionales
1. **Modelo de Datos (`VisualizacionVideo`):**
   - RelaciÃ³n con `User` (Estudiante).
   - RelaciÃ³n con `VideoTema` (Video).
   - `contador`: NÃºmero entero que se incrementa cada vez que el video finaliza.
   - `fecha_primera_vista`: Fecha y hora del primer registro.
   - `fecha_ultima_vista`: Fecha y hora de la mÃ¡s reciente finalizaciÃ³n del video.
2. **Registro de VisualizaciÃ³n (Backend):**
   - Crear una vista (endpoint AJAX) que reciba el ID del video.
   - Si no existe un registro previo para el Usuario-Video, crearlo con contador = 1.
   - Si existe, incrementar el contador y actualizar `fecha_ultima_vista`.
   - Validar que el usuario estÃ© autenticado y tenga permiso (tema recomendado).
3. **Trigger de Registro (Frontend):**
   - En el template de videos, capturar el evento `ended` del elemento `<video>`.
   - Al finalizar el video, realizar una peticiÃ³n POST asÃ­ncrona (Fetch API) al endpoint de registro.
4. **AdministraciÃ³n (Django Admin):**
   - Mostrar una lista de todas las relaciones Usuario-Video registradas.
   - La lista debe incluir: Usuario, TÃ­tulo del Video, Grado, SecciÃ³n, Contador y Ãšltima VisualizaciÃ³n.
   - Permitir filtrar por Grado, SecciÃ³n y Video.

## Requerimientos No Funcionales
- **Integridad:** Asegurar que el contador se actualice correctamente incluso ante mÃºltiples finalizaciones.
- **Eficiencia:** El registro AJAX debe ser rÃ¡pido y no interrumpir la experiencia del usuario.
- **Consistencia:** Mantener el idioma espaÃ±ol en todos los mensajes y etiquetas.

## Criterios de AceptaciÃ³n
- [ ] Al terminar de reproducir un video (evento `ended`), se envÃ­a una peticiÃ³n al servidor.
- [ ] La base de datos registra una nueva visualizaciÃ³n o incrementa el contador existente.
- [ ] El administrador puede ver el reporte de vistas con grado y secciÃ³n del estudiante.
- [ ] No se registran vistas si el video no llega a su fin (segÃºn el evento del navegador).

## Fuera de Alcance
- Registro de tiempo exacto de reproducciÃ³n (segundos vistos).
- Reportes visuales con grÃ¡ficos (analÃ­tica avanzada).
- Control de "visto" para desbloquear otros contenidos.
