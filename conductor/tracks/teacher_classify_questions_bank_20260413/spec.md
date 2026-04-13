# Especificación del Track: HU32 - Clasificar Preguntas por Tema y Nivel

## 1. Visión General
Este track tiene como objetivo estandarizar y mejorar la organización del banco de problemas y el examen diagnóstico. Se implementará una clasificación rigurosa por tema y nivel de dificultad en todas las estructuras de preguntas, facilitando su gestión mediante filtros interactivos en el panel docente y preparando la base para la futura selección adaptativa.

## 2. Requerimientos Funcionales

### 2.1 Estandarización de Modelos
- **Modelo Ejercicio (Consolidación):** Validar que los campos `tema` (FK) y `dificultad` sean obligatorios y consistentes.
- **Modelo Pregunta (Alineación):** Actualizar el modelo de examen diagnóstico para que use el modelo `Tema` en lugar de un campo de texto plano (`categoria`) y añadir el campo `dificultad` (Básico, Intermedio, Avanzado).

### 2.2 Gestión y Organización (UI Docente)
- **Filtros en Listado de Banco:** Añadir selectores de "Tema" y "Dificultad" en la vista `BancoPreguntasListView` para permitir búsquedas rápidas.
- **Formularios:** Asegurar que los campos de clasificación estén resaltados y validados tanto en la creación como en la edición de preguntas.

### 2.3 Persistencia e Integridad
- Las migraciones deben manejar la transición de datos existentes (ej: convertir `categoria` de texto a FK de `Tema` si es posible).
- Garantizar que ningún ejercicio o pregunta quede sin clasificación tras la implementación.

## 3. Requerimientos Técnicos
- **Modelos:** Actualizar `AppEvaluar.Pregunta` para incluir `dificultad` y cambiar `categoria` por `tema` (FK a `AppTutoria.Tema`).
- **Backend:** Actualizar `BancoPreguntasListView` en `AppEvaluar/views.py` para soportar filtrado vía parámetros GET.
- **Frontend:** Actualizar `banco_preguntas_list.html` con una barra de filtros moderna y coherente con el estilo de reportes.

## 4. Criterios de Aceptación
- **Escenario: Clasificación de Diagnóstico:** El docente puede asignar tema y dificultad a una pregunta del examen diagnóstico.
- **Escenario: Filtrado Eficiente:** El docente selecciona "Triángulos" y "Intermedio" en el listado y el sistema muestra solo los ejercicios que cumplen ambos criterios.
- **Escenario: Consistencia de Datos:** Toda pregunta guardada persiste correctamente su tema y nivel en PostgreSQL.

## 5. Fuera de Alcance
- Motor de selección adaptativa en tiempo real (solo se deja la base de datos lista).
- Reestructuración completa del examen diagnóstico fuera de estos campos.
