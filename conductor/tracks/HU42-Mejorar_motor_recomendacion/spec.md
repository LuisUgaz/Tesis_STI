# Especificación: Mejora del Motor de Recomendación Adaptativa (HU42)

## 1. Descripción General
Se actualizará el sistema de recomendación actual para que no solo considere el porcentaje de aciertos, sino que evalúe la calidad del desempeño del estudiante mediante un **Puntaje de Desempeño Ponderado (PDP)**. Este puntaje integrará la dificultad de las preguntas, el tiempo de respuesta y utilizará un clasificador **SVM (Support Vector Machine)** para resolver empates técnicos entre temas, asegurando una personalización más precisa.

## 2. Requisitos Funcionales

### 2.1 Captura de Datos Multidimensionales
- **Tiempo de Respuesta:** Modificar el modelo `RespuestaUsuario` para registrar el tiempo en segundos que el estudiante tardó en responder cada pregunta.
- **Dificultad de Pregunta:** Utilizar el campo `dificultad` existente en el modelo `Pregunta` (Básico, Intermedio, Avanzado).

### 2.2 Algoritmo de Puntaje de Desempeño Ponderado (PDP)
- **Ponderación de Fallos:**
    - Error en pregunta **Básica**: Penalización de factor 3.
    - Error en pregunta **Intermedia**: Penalización de factor 2.
    - Error en pregunta **Avanzada**: Penalización de factor 1.
- **Penalización por Tiempo:**
    - Si el tiempo de respuesta en una respuesta correcta es significativamente superior al promedio estadístico (Relativo), se aplicará una reducción proporcional en el PDP del tema.

### 2.3 Clasificador SVM (Desempate)
- **Activación:** Se invoca únicamente cuando dos o más temas obtienen el mismo PDP más bajo.
- **Características (Features):**
    - Tiempo promedio global del estudiante.
    - Nivel de dificultad actual del perfil.
    - Puntaje del tema en disputa.
- **Persistencia:** El modelo SVM se integrará directamente en el código del servicio de recomendación, sin dependencias de configuración dinámica en base de datos.
- **Fallback:** Si los datos son insuficientes para el SVM, se utilizará el orden alfabético.

### 2.4 Integración con HU15 (Ajuste de Dificultad)
- El nivel de dificultad inicial del estudiante (`profile.nivel_dificultad_actual`) se actualizará basándose en el tema con el PDP más bajo obtenido en el diagnóstico.

## 3. Criterios de Aceptación

### Escenario: Generación de recomendación con múltiples variables
- **Dado** que un estudiante ha finalizado su examen diagnóstico.
- **Cuando** el sistema procesa los resultados.
- **Entonces** debe calcular un Puntaje de Desempeño Ponderado por tema.
- **Y** los fallos en preguntas básicas deben penalizar más (x3) que en avanzadas (x1).
- **Y** el tiempo excesivo en respuestas correctas debe influir negativamente.

### Escenario: Desempate mediante SVM
- **Dado** un empate en el PDP de dos temas.
- **Cuando** se solicita la recomendación.
- **Entonces** el sistema debe invocar el clasificador SVM integrado.
- **Y** elegir el tema prioritario basándose en el contexto del estudiante.

## 4. Alcance (In-Scope)
- Modificación de modelos (`RespuestaUsuario`).
- Actualización de `AppEvaluar/services.py` con la nueva lógica PDP y SVM.
- Pruebas unitarias de desempate y validación de ponderación.

## 5. Fuera de Alcance (Out-of-Scope)
- Rediseño de la interfaz de usuario (UI).
- Entrenamiento en tiempo real del modelo SVM (se usará uno pre-configurado).
- Cambios en el sistema de insignias o puntos de gamificación.
