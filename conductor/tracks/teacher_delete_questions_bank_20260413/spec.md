# Especificación del Track: HU31 - Eliminar Preguntas del Banco

## 1. Visión General
Este track tiene como objetivo implementar la funcionalidad de retiro de problemas geométricos del banco de práctica. El módulo permitirá a los usuarios con rol **Docente** desactivar preguntas que ya no se consideren útiles, asegurando la integridad de los resultados históricos mediante una estrategia de eliminación lógica (Soft Delete).

## 2. Requerimientos Funcionales

### 2.1 Módulo de Gestión de Preguntas (Ampliación)
- **Acceso Restringido:** Solo para usuarios con rol **Docente**.
- **Integración en Listado:** Añadir una columna de "Acciones" (o ampliar la existente) en `AppEvaluar/banco_preguntas_list.html` con un botón/icono para eliminar.
- **Mecanismo de Confirmación:** Implementar un modal de Bootstrap que advierta al docente sobre la acción y solicite confirmación explícita.

### 2.2 Lógica de Eliminación (Soft Delete)
- **Estrategia Segura:** En lugar de borrar físicamente el registro de la base de datos, se utilizará un campo `activo` (o similar) para marcar la pregunta como retirada.
- **Preservación Histórica:** Los registros en `ResultadoEjercicio` y `ResultadoDiagnostico` vinculados a la pregunta deben mantenerse intactos para no alterar las métricas de los estudiantes.
- **Filtrado Automático:** Una vez "eliminada", la pregunta no debe volver a aparecer en:
    - Sesiones de práctica del estudiante.
    - El listado de gestión por defecto del docente (opcional: añadir filtro para ver eliminadas).

### 2.3 Persistencia y Mensajería
- Actualización del estado del `Ejercicio` tras la confirmación.
- Notificación de éxito mediante un mensaje emergente (Success Toast/Alert).
- Redirección o refresco asíncrono del listado de preguntas.

## 3. Requerimientos Técnicos
- **Modelos:** Añadir campo `es_activo` (BooleanField, default=True) al modelo `AppEvaluar.Ejercicio`.
- **Backend:** Vista de Django `BancoPreguntasDeleteView` que herede de `DeleteView` o una vista personalizada que implemente la lógica de desactivación.
- **Frontend:** Actualización de `banco_preguntas_list.html` con el modal de confirmación y lógica JavaScript/AJAX para el envío.

## 4. Criterios de Aceptación
- **Escenario: Eliminación lógica exitosa:** El docente selecciona eliminar, confirma en el modal, la pregunta desaparece del listado y los estudiantes ya no la reciben en sus prácticas, pero sus resultados previos siguen visibles en sus perfiles.
- **Escenario: Acceso prohibido:** Un estudiante intenta invocar la acción de eliminación y el sistema devuelve un error 403.
- **Escenario: Manejo de inexistencia:** Intentar eliminar una ID no válida redirige al listado con un mensaje de error controlado.

## 5. Fuera de Alcance
- Papelera de reciclaje con interfaz de restauración.
- Eliminación física masiva de datos históricos.
