# Specification: HU40 - Generar retroalimentación inteligente al finalizar el examen diagnóstico

## Descripción General
Esta tarea implementa un sistema de retroalimentación inteligente basado en IA (Gemini 1.5 Flash) que se dispara tras finalizar el examen diagnóstico. El objetivo es proporcionar al estudiante una explicación pedagógica personalizada para cada pregunta, ayudándole a comprender sus aciertos y errores en geometría de nivel secundaria.

## Requisitos Funcionales

### 1. Interacción de Envío
- **Modal de Confirmación:** Antes de procesar el envío del examen, se debe mostrar un modal preguntando al estudiante si está seguro de finalizar.
- **Indicador de Procesamiento:** Una vez confirmado, se mostrará un **Overlay Bloqueante** con un indicador de carga (spinner) mientras el servidor registra las respuestas y calcula el puntaje inicial.

### 2. Generación de Retroalimentación (IA)
- **Orquestador Backend:** Un nuevo endpoint en Django recibirá las solicitudes AJAX para generar explicaciones.
- **Contexto de IA:** Para cada pregunta, el backend construirá un prompt para Gemini 1.5 Flash incluyendo:
    - Enunciado de la pregunta.
    - Imagen asociada (si existe).
    - Opción seleccionada por el alumno.
    - Respuesta correcta del sistema.
    - Tema y dificultad.
- **Perfil del Tutor:** La IA debe actuar como un tutor de geometría de secundaria: tono motivador, lenguaje claro y explicaciones breves (máximo 3 líneas).
    - **Aciertos:** Felicitar y reforzar el concepto.
    - **Errores:** Explicar el fallo de razonamiento y guiar hacia la lógica correcta.

### 3. Visualización de Resultados
- **Carga Diferida (AJAX):** La página de resultados se cargará inmediatamente con la nota y el desglose de preguntas. Las explicaciones de la IA se solicitarán asíncronamente desde el frontend.
- **Componente UI:** La retroalimentación de la IA se mostrará dentro de un **Acordeón (Colapsable)** debajo de cada pregunta, identificado claramente como "Explicación del Tutor IA".
- **Manejo de Errores (Fallback):** Si la API de Gemini falla o el tiempo de espera se agota, se mostrará el mensaje: *"No se pudo generar la explicación IA"*.

## Requisitos No Funcionales
- **Seguridad:** El acceso al endpoint de generación de IA debe estar restringido a usuarios autenticados y solo para sus propios exámenes.
- **Rendimiento:** Uso de Gemini 1.5 Flash para minimizar la latencia.
- **Privacidad:** No se deben enviar datos personales del estudiante a la IA, solo el contexto académico de la pregunta.

## Criterios de Aceptación
- [ ] El estudiante ve un modal de confirmación al intentar enviar el examen.
- [ ] Se muestra un overlay de carga mientras se procesa el registro inicial del examen.
- [ ] La página de resultados muestra la nota global sin esperar a la IA.
- [ ] Las explicaciones de la IA aparecen de forma asíncrona (AJAX) debajo de cada pregunta.
- [ ] Las explicaciones son pedagógicas y se presentan en un componente colapsable.
- [ ] El sistema maneja correctamente preguntas con y sin imágenes.
- [ ] Se muestra un mensaje de error amigable si el servicio de IA no responde.

## Fuera de Alcance
- Chat interactivo con la IA.
- Recálculo de notas basado en el criterio de la IA.
- Generación de nuevas preguntas.
