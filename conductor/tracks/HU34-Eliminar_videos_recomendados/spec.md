# Especificación: HU34 - Eliminar videos recomendados

## Visión General
Permitir que los docentes y administradores eliminen videos recomendados del catálogo del sistema para mantener el material de apoyo actualizado, asegurando que los registros históricos de visualización no se vean afectados mediante la implementación de un borrado lógico.

## Requisitos Funcionales
- **RF-1: Opción de Eliminación**: El sistema debe mostrar una opción para eliminar videos en la vista de gestión de videos (`video_gestion_list.html`).
- **RF-2: Restricción de Acceso**: Solo los usuarios con rol de docente o administrador podrán acceder a la funcionalidad de eliminación.
- **RF-3: Confirmación de Eliminación**: Antes de proceder con la eliminación, el sistema debe mostrar un modal de confirmación simple con las opciones "Confirmar" y "Cancelar".
- **RF-4: Borrado Lógico (Soft Delete)**: Al confirmar la eliminación, el video no se borrará físicamente de la base de datos. Se marcará como inactivo (mediante un campo `es_activo` o similar) para no romper la integridad referencial de los registros de visualización existentes.
- **RF-5: Actualización del Catálogo**: Una vez marcado como inactivo, el video ya no debe aparecer en los listados visibles para los estudiantes ni en la gestión activa del docente.
- **RF-6: Persistencia de Archivos**: Los archivos físicos (video .mp4 y miniaturas) se mantendrán en el servidor para evitar errores en registros históricos que dependan de esas rutas.

## Requisitos No Funcionales
- **RNF-1: Integridad de Datos**: La eliminación lógica no debe causar errores en cascada ni borrar registros de la tabla de visualizaciones (`VisualizacionVideo`).
- **RNF-2: Experiencia de Usuario**: La acción de eliminar debe ser fluida, refrescando la vista tras la confirmación exitosa.

## Criterios de Aceptación
- **Escenario: Eliminación Exitosa**
    - **Dado** que un docente/administrador está en la lista de gestión de videos.
    - **Cuando** selecciona la opción de eliminar un video y confirma en el modal.
    - **Entonces** el sistema marca el video como inactivo.
    - **Y** el video desaparece de la lista de gestión.
    - **Y** el video desaparece de la vista del estudiante.
    - **Y** los registros de visualizaciones previas del video se mantienen intactos en la base de datos.

## Fuera de Alcance
- Recuperación de videos eliminados (deshacer borrado/papelera de reciclaje).
- Versionado de recursos multimedia.