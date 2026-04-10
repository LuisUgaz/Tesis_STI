# Especificación del Track: HU12 - Visualización de Videos Recomendados

## Información General
- **ID del Track:** user_view_recommended_videos_20260410
- **Descripción:** Implementar la visualización de videos educativos recomendados para reforzar el aprendizaje de temas geométricos.
- **Tipo:** Feature
- **Usuario Principal:** Estudiante

## Objetivos
- Proporcionar a los estudiantes recursos audiovisuales específicos para los temas que necesitan reforzar.
- Mantener una interfaz moderna y organizada que facilite el acceso a contenido multimedia.

## Requerimientos Funcionales
1. **Modelo de Datos (VideoTema):**
   - Título del video.
   - Archivo de video (Upload local).
   - Imagen de miniatura (Thumbnail).
   - Descripción corta.
   - Duración aproximada (Ej: "5:30 min").
   - Orden/Prioridad (para organizar la lista).
   - Relación con el modelo `Tema`.
2. **Vista de Videos:**
   - Crear una nueva vista independiente que reciba el `slug` del tema.
   - Filtrar videos asociados al tema solicitado.
   - Validar que el estudiante tenga acceso al tema (basado en recomendaciones).
3. **Interfaz de Usuario (UI):**
   - Grilla de tarjetas (Cards) moderna.
   - Cada tarjeta debe mostrar: Miniatura, Título, Duración, Descripción corta y un botón de reproducción.
   - Navegación de regreso al detalle del tema o a la lista general.
4. **Integración:**
   - Habilitar el enlace "Videos" en el Sidebar de la vista `tema_detalle`.

## Requerimientos No Funcionales
- **Diseño Adaptativo (Responsive):** La grilla de videos debe ajustarse a dispositivos móviles y tablets.
- **Consistencia Visual:** Usar la paleta de colores y estilos definidos en el sistema (CSS variables).
- **Usabilidad:** Los videos deben cargarse de forma fluida y ser fáciles de identificar.

## Criterios de Aceptación
- [ ] El sistema permite cargar videos desde el administrador de Django asociados a temas específicos.
- [ ] El estudiante puede acceder a la sección de videos desde el detalle de un tema recomendado.
- [ ] Los videos se muestran en una grilla de tarjetas organizada por el campo "orden".
- [ ] El video se puede reproducir correctamente en la interfaz (usando tag `<video>` de HTML5).

## Fuera de Alcance
- Registro de visualizaciones (saber si el estudiante vio el video completo).
- Comentarios o valoraciones en los videos.
- Gestión de videos desde el perfil del estudiante (solo Admin).
