# Track Specification - HU21 - Visualizar mÃ©tricas de desempeÃ±o

## Overview
Esta historia de usuario implementa la interfaz visual necesaria para que el estudiante consulte sus indicadores de desempeÃ±o acadÃ©mico acumulados. Tras el cÃ¡lculo automatizado realizado en la HU20, el estudiante requiere un panel amigable ("Dashboard") que traduzca esos nÃºmeros en una visiÃ³n clara de su progreso, dominios y Ã¡reas de refuerzo.

## Functional Requirements
- **PÃ¡gina Independiente "Mi Progreso":** CreaciÃ³n de una nueva vista dedicada accesible mediante una ruta especÃ­fica (ej: `/usuarios/mi-progreso/`).
- **IntegraciÃ³n en MenÃº Principal:** AÃ±adir la opciÃ³n "Mi progreso" en la barra de navegaciÃ³n lateral o superior, visible solo para usuarios con rol 'Estudiante'.
- **VisualizaciÃ³n de MÃ©tricas Globales:** 
  - **Tarjetas de Resumen:** Mostrar con nÃºmeros grandes y etiquetas: PrecisiÃ³n General (%), Rendimiento AcadÃ©mico (Promedio) y Tiempo Medio de Respuesta.
  - **GamificaciÃ³n:** Uso de iconos (ej: estrellas para alto rendimiento, relojes para tiempo) para motivar al estudiante.
- **Desglose Detallado por Temas:** 
  - Listado de todos los temas registrados (TriÃ¡ngulos, Ãngulos, etc.).
  - **Barras de Progreso:** RepresentaciÃ³n visual del porcentaje de dominio para cada categorÃ­a.
- **Seguridad:** La pÃ¡gina debe estar restringida para que el estudiante solo vea sus propias mÃ©tricas (LoginRequired + Rol Validation).

## UI/UX Design
- **EstÃ©tica Gamificada:** Consistente con el estilo del sistema (colores vibrantes, tarjetas con sombras suaves).
- **Responsive:** El panel debe ser legible tanto en escritorio como en dispositivos mÃ³viles.
- **Mensajes de VacÃ­o:** Si no hay mÃ©tricas calculadas aÃºn, mostrar un mensaje motivador invitando a realizar actividades.

## Acceptance Criteria
- Existe una nueva URL y vista para "Mi Progreso".
- El menÃº principal incluye el acceso directo.
- Se visualizan correctamente los datos del modelo `MetricasEstudiante`.
- Los porcentajes se muestran con barras de progreso funcionales.
- Solo el usuario logueado puede ver sus datos.

## Out of Scope
- Funcionalidad de recÃ¡lculo (se asume que HU20 ya lo hace).
- Comparativas con otros alumnos o rankings.
- ExportaciÃ³n de los indicadores a PDF.
