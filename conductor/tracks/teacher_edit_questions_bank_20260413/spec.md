# Especificación del Track: HU30 - Editar Preguntas del Banco

## 1. Visión General
Este track tiene como objetivo implementar la funcionalidad de edición de problemas geométricos existentes en el banco de práctica. El módulo permitirá a cualquier usuario con rol **Docente** actualizar enunciados, temas, niveles de dificultad, explicaciones técnicas y las 5 opciones de respuesta asociadas, garantizando la integridad de los datos y la persistencia de los cambios.

## 2. Requerimientos Funcionales

### 2.1 Módulo de Gestión de Preguntas
- **Acceso Restringido:** Solo para usuarios con rol **Docente**.
- **Vista de Listado:** Implementar una nueva vista tipo tabla que enumere todas las preguntas registradas en el banco (`Ejercicio`).
    - Columnas sugeridas: Enunciado (resumen), Tema, Dificultad, Fecha de Creación.
    - Acciones: Botón "Editar" por cada fila.

### 2.2 Formulario de Edición de Pregunta
- **Carga de Datos:** Al acceder, el formulario debe precargarse con la información actual del `Ejercicio` y sus 5 `OpcionEjercicio`.
- **Campos Editables:**
    - Texto de la pregunta, Tema (Selección), Nivel de Dificultad, Explicación Técnica e Imagen.
    - Los campos de texto, selección y correctitud de las 5 opciones.
- **Validación de Integridad:**
    - Exactamente una opción debe marcarse como correcta.
    - Se debe mantener estrictamente la cantidad de **5 opciones** por ejercicio.
    - Validación de campos obligatorios (Texto, Tema, Dificultad).

### 2.3 Persistencia
- Actualización atómica (Ejercicio + Opciones) para evitar estados inconsistentes.
- Mensaje de confirmación (Success Message) tras una edición exitosa.
- Redirección automática al Listado de Gestión.

## 3. Requerimientos Técnicos
- **Frontend:** Nuevo template `AppEvaluar/banco_preguntas_list.html` y un template específico de edición `AppEvaluar/banco_preguntas_edit.html` (basado en el estilo moderno del docente).
- **Backend:** Vista de Django `BancoPreguntasUpdateView` (CBV) y una nueva `BancoPreguntasListView`.
- **Modelos:** Reutilización de `AppEvaluar.Ejercicio` y `AppEvaluar.OpcionEjercicio`.
- **Formularios:** Reutilización de `EjercicioForm` y `OpcionEjercicioFormSet`.

## 4. Criterios de Aceptación
- **Escenario: Edición exitosa:** El docente modifica el texto de una pregunta y su respuesta correcta, guarda y el cambio persiste en la base de datos y se refleja en las prácticas de los estudiantes.
- **Escenario: Acceso prohibido:** Un estudiante intenta acceder a la URL de edición o listado y recibe un error 403.
- **Escenario: Validación de opciones:** El sistema impide guardar si no hay exactamente una opción correcta marcada.

## 5. Fuera de Alcance
- Eliminación de preguntas.
- Clasificación avanzada o etiquetado personalizado.
- Edición de preguntas del Examen Diagnóstico.
