# Especificación del Track: HU15 - Ajuste de dificultad adaptativa

## Información General
- **ID del Track:** user_adaptive_difficulty_20260410
- **Descripción:** Implementar la lógica para ajustar automáticamente la dificultad de los ejercicios (Básico, Intermedio, Avanzado) según el rendimiento del estudiante al finalizar cada sesión de práctica.
- **Tipo:** Feature
- **Usuario Principal:** Estudiante / Sistema

## Objetivos
- Adaptar el desafío educativo al nivel real de competencia del estudiante.
- Proporcionar una progresión estable basada en el desempeño de sesiones completas.
- Personalizar el punto de partida según los resultados del diagnóstico inicial.

## Requerimientos Funcionales
1. **Modelado y Persistencia:**
   - Añadir el campo `nivel_dificultad_actual` al modelo `Profile` en `AppGestionUsuario`.
   - Valores posibles: 'Básico', 'Intermedio', 'Avanzado'.
2. **Determinación del Nivel Inicial:**
   - Al procesar el examen diagnóstico (HU05/HU06), asignar el nivel inicial en el `Profile`.
   - Regla propuesta: 0-40% (Básico), 41-75% (Intermedio), 76-100% (Avanzado).
3. **Lógica de Adaptación (Post-Sesión):**
   - Al finalizar una sesión de ejercicios (HU14), calcular el porcentaje de aciertos.
   - **Subir Nivel:** Si el acierto es >= 80% y el nivel actual no es 'Avanzado', subir al siguiente nivel.
   - **Mantener/Bajar Nivel:** Si el acierto es < 80%, mantener el nivel actual.
4. **Integración con Selección de Ejercicios:**
   - Modificar la vista `iniciar_practica` para que filtre los ejercicios no solo por `Tema`, sino también por el `nivel_dificultad_actual` del perfil del estudiante.

## Requerimientos No Funcionales
- **Encapsulamiento:** La lógica de ajuste debe estar en un servicio o método dedicado para facilitar cambios futuros en las reglas heurísticas.
- **Transparencia:** El sistema debe ser capaz de informar al estudiante (opcionalmente) que su nivel ha cambiado al finalizar la sesión.

## Criterios de Aceptación
- [ ] El perfil del estudiante almacena su nivel actual de dificultad.
- [ ] El nivel inicial se asigna correctamente tras el examen diagnóstico.
- [ ] Al terminar una sesión de 5 ejercicios con 4 o 5 correctos (>=80%), el nivel en el perfil aumenta.
- [ ] La siguiente sesión de práctica carga ejercicios del nuevo nivel de dificultad.

## Fuera de Alcance
- IA Generativa para crear ejercicios.
- Ajuste de dificultad a mitad de una sesión.
- Notificaciones push sobre el cambio de nivel.
