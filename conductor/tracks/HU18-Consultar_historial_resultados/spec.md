# Track Specification - HU18 - Consultar historial de resultados

## Overview
Esta historia de usuario permite a los estudiantes consultar su historial completo de actividades y resultados acadÃ©micos dentro del Sistema Tutor Inteligente Adaptativo. El objetivo es proporcionar una visiÃ³n clara de su evoluciÃ³n, incluyendo el examen diagnÃ³stico, ejercicios resueltos y progreso en temas teÃ³ricos o visualizaciÃ³n de videos.

## Functional Requirements
- **Acceso desde Perfil:** El estudiante podrÃ¡ acceder a su historial mediante un botÃ³n ubicado en su perfil de usuario.
- **VisualizaciÃ³n en Nueva PestaÃ±a:** Al hacer clic en el botÃ³n, el historial se abrirÃ¡ en una nueva pestaÃ±a del navegador.
- **Tabla de Resultados:** Los datos se presentarÃ¡n en una tabla organizada con las siguientes columnas (sugeridas):
  - Fecha (DÃ­a/Hora).
  - Tema (TriÃ¡ngulos, Ãngulos, etc.).
  - Actividad (Ejercicio, Video, TeorÃ­a, Examen).
  - Resultado/Detalle (Puntaje, Correcto/Incorrecto, Completado).
- **Ordenamiento y Filtros:** 
  - El sistema permitirÃ¡ ordenar los registros cronolÃ³gicamente (mÃ¡s reciente primero por defecto).
  - El sistema permitirÃ¡ filtrar los resultados por el Tema de geometrÃ­a.
- **NavegaciÃ³n de Retorno:** La vista del historial incluirÃ¡ un botÃ³n prominente para cerrar o regresar a la pestaÃ±a del perfil del usuario.
- **Privacidad de Datos:** Un estudiante solo podrÃ¡ visualizar su propio historial de actividades.

## Data Sources
- `ProgresoEstudiante`: Para el historial general de actividades (Video, TeorÃ­a, Ejercicio, Examen).
- `ResultadoDiagnostico`: Para obtener el puntaje especÃ­fico del examen inicial.
- `ResultadoEjercicio`: Para mostrar si un ejercicio especÃ­fico fue resuelto correctamente y el feedback recibido.

## Acceptance Criteria
- El estudiante visualiza una tabla con su historial completo.
- Los registros estÃ¡n ordenados cronolÃ³gicamente de forma predeterminada.
- Es posible filtrar por tema.
- El acceso se realiza desde el perfil y se abre en una nueva pestaÃ±a.
- Existe un botÃ³n para regresar al perfil.
- No se muestran datos de otros estudiantes.

## Out of Scope
- Filtros avanzados por rango de fechas (fuera de lo cronolÃ³gico simple).
- ExportaciÃ³n de reportes (PDF/Excel).
- GrÃ¡ficos de mÃ©tricas agregadas.
- EdiciÃ³n o eliminaciÃ³n de registros del historial.
