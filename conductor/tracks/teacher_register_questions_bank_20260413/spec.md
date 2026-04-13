# Especificación del Track: HU29 - Registrar Preguntas en Banco

## 1. Visión General
Este track tiene como objetivo implementar la funcionalidad de registro de nuevos problemas geométricos para el banco de práctica del sistema. El módulo permitirá a los docentes ampliar el contenido educativo sin necesidad de acceder al administrador de Django, facilitando la gestión de ejercicios personalizados por tema y dificultad.

## 2. Requerimientos Funcionales

### 2.1 Módulo de Banco de Problemas
- Acceso restringido para usuarios con el rol **Docente**.
- Interfaz dedicada en el panel analítico del docente (Sección independiente).

### 2.2 Formulario de Registro de Pregunta
- Campos obligatorios para el modelo `Ejercicio`:
    - **Texto de la pregunta:** Contenido principal del problema geométrico.
    - **Tema/Categoría:** Selección basada en los temas existentes (ej: Triángulos, Ángulos).
    - **Nivel de Dificultad:** Selector con opciones: Básico, Intermedio, Avanzado.
    - **Explicación Técnica:** Fundamento teórico para la retroalimentación inmediata.
- Campos para el modelo `OpcionEjercicio`:
    - Registro de exactamente **5 opciones** por pregunta.
    - Cada opción debe tener un campo de texto y un selector para marcar si es la correcta.
    - **Regla:** Exactamente una opción debe ser marcada como correcta.
    - Campo opcional de retroalimentación específica por opción.

### 2.3 Persistencia y Validación
- El sistema debe validar que todos los campos obligatorios estén presentes.
- Al guardar, se creará un registro en el modelo `Ejercicio` y cinco registros asociados en el modelo `OpcionEjercicio`.
- Los ejercicios registrados deben ser inmediatamente utilizables en el mÃ³dulo de prÃ¡ctica del estudiante.

## 3. Requerimientos Técnicos
- **Frontend:** Formulario HTML interactivo integrado en la UI docente existente.
- **Backend:** Vista de Django (CBV o FBV) con validación de formularios y manejo de transacciones para asegurar la integridad (Ejercicio + Opciones).
- **Modelos:** Reutilización de `AppEvaluar.Ejercicio` y `AppEvaluar.OpcionEjercicio`.

## 4. Criterios de Aceptación
- **Escenario: Registro exitoso:** El docente ingresa los datos, marca una opción correcta y el ejercicio se guarda correctamente.
- **Escenario: Validación de campos:** El sistema impide guardar si falta el texto, el tema o si no se ha marcado ninguna opción como correcta.
- **Escenario: Reutilización:** Un estudiante que practica el tema seleccionado puede recibir el nuevo ejercicio de forma aleatoria si coincide con su nivel.

## 5. Fuera de Alcance
- Edición de preguntas ya registradas.
- Eliminación de preguntas.
- Registro de preguntas para el Examen Diagnóstico (`Pregunta`/`Opcion`).
- Clasificación avanzada o etiquetas personalizadas fuera de los temas base.
