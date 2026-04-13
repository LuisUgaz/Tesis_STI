# Track Specification - HU25 - Visualizar insignias obtenidas

## Overview
Esta funcionalidad mejora la colecciÃ³n de logros del estudiante, permitiÃ©ndole consultar de forma detallada sus insignias ganadas. Se implementarÃ¡ una interfaz interactiva donde el estudiante podrÃ¡ ver su historial de Ã©xitos, incluyendo descripciones y fechas de obtenciÃ³n, mientras que las insignias no alcanzadas servirÃ¡n como recordatorios visuales de metas futuras.

## Functional Requirements
- **GalerÃ­a Interactiva:**
  - Mostrar todas las insignias del sistema en el perfil del estudiante.
  - Las insignias obtenidas se muestran a color; las no obtenidas en escala de grises.
- **Detalle de Logro (Modal):**
  - Al hacer clic en una insignia ganada, abrir un Modal con:
    - Icono y Nombre de la insignia.
    - DescripciÃ³n completa del logro.
    - Fecha y hora exacta de obtenciÃ³n.
- **Ordenamiento DinÃ¡mico:**
  - Listar las insignias priorizando las mÃ¡s recientes ganadas por el usuario actual.
- **Seguridad de Consulta:**
  - Asegurar que el estudiante solo pueda ver sus propias insignias (validaciÃ³n de usuario en la vista).

## Technical Constraints
- Utilizar el modelo `LogroEstudiante` creado en HU24 para extraer las fechas de obtenciÃ³n.
- El Modal debe ser implementado con Vanilla JavaScript y CSS para mantener consistencia con el proyecto.
- El filtro de escala de grises debe aplicarse mediante CSS (`filter: grayscale(100%)`).

## Acceptance Criteria
- El estudiante visualiza su colecciÃ³n completa al ingresar a su perfil.
- Las insignias ganadas aparecen resaltadas y permiten abrir el modal de detalle.
- El modal muestra correctamente la fecha en que se obtuvo la insignia.
- Las insignias de otros estudiantes no son accesibles para el usuario actual.

## Out of Scope
- Funcionalidad de "Insignia Favorita" para destacar en el encabezado.
- Animaciones complejas de apertura de modal.
