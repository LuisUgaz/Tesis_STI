# Especificación de Pista (Track): HU16 - Retroalimentación Inmediata

## 1. Visión General
El objetivo de esta pista es mejorar la experiencia de aprendizaje del estudiante mediante la entrega de retroalimentación detallada y visualmente atractiva tras resolver un ejercicio. A diferencia de la implementación básica actual, se busca un enfoque "mixto" que explique por qué una opción es incorrecta (específico de la opción) y proporcione el fundamento teórico correcto (general del ejercicio).

## 2. Requerimientos Funcionales
- **RF1: Almacenamiento de Explicación General:** El sistema debe permitir registrar una explicación técnica general para cada ejercicio en el banco de problemas.
- **RF2: Validación con Feedback Mixto:** Al enviar una respuesta, el sistema debe retornar:
    - Estado (Correcto/Incorrecto).
    - Feedback específico de la opción seleccionada.
    - Explicación técnica general del ejercicio.
- **RF3: Interfaz con Iconografía:** El área de feedback debe mostrar iconos (Ej: ✅ para aciertos, ❌ para errores, 💡 para explicaciones) y usar tarjetas con bordes destacados.
- **RF4: Persistencia de Feedback:** El resultado guardado en `ResultadoEjercicio` debe incluir la concatenación de ambos feedbacks (específico + general) para auditoría docente.

## 3. Requerimientos No Funcionales
- **RNF1: Asincronía (AJAX):** La validación debe ser instantánea sin recargar la página (reutilizando la lógica AJAX existente).
- **RNF2: Consistencia Visual:** El diseño debe integrarse con el estilo actual de `practica_ejercicio.html`.

## 4. Criterios de Aceptación
- **Escenario: Feedback Mixto tras Responder**
    - **Dado** que el estudiante selecciona una opción en un ejercicio de práctica.
    - **Cuando** presiona el botón "Validar".
    - **Entonces** el sistema debe mostrar una tarjeta con el estado (Correcto/Incorrecto).
    - **Y** debe mostrar el mensaje de retroalimentación de la opción elegida.
    - **Y** debe mostrar la explicación técnica general del ejercicio.
    - **Y** debe usar iconos representativos según el resultado.

## 5. Fuera de Alcance
- Tutor conversacional inteligente.
- Recomendación automática del siguiente tema (cubierto por otras HU).
- Gamificación inmediata (puntos flotando, etc.).
