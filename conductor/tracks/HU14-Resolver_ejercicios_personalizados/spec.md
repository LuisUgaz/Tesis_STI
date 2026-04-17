# Especificación del Track: HU14 - Resolver ejercicios personalizados

## Información General
- **ID del Track:** user_resolve_custom_exercises_20260410
- **Descripción:** Implementar un sistema de práctica con ejercicios personalizados de opción múltiple, adaptados al nivel de desempeño del estudiante.
- **Tipo:** Feature
- **Usuario Principal:** Estudiante

## Objetivos
- Proporcionar ejercicios específicos según el tema recomendado y el nivel del estudiante.
- Permitir la resolución secuencial de ejercicios con corrección automática.
- Persistir los resultados de la práctica para seguimiento del progreso.

## Requerimientos Funcionales
1. **Modelado de Datos (Nuevos Modelos):**
   - `Ejercicio`: Vinculado a `Tema`, con campos para `texto`, `dificultad` (Básico, Intermedio, Avanzado) e imagen opcional.
   - `OpcionEjercicio`: Opciones vinculadas a un `Ejercicio`, indicando cuál es la correcta.
   - `ResultadoEjercicio`: Registro de la resolución (Usuario, Ejercicio, si fue correcto, tiempo empleado y feedback mostrado).
2. **Lógica de Selección:**
   - Al acceder a la sección de ejercicios, el sistema filtrará los ejercicios por el `Tema` actualmente recomendado para el estudiante.
   - Se seleccionará un conjunto de ejercicios acordes al nivel de desempeño previo (o nivel base si es nuevo).
3. **Interfaz de Usuario (UI):**
   - Visualización secuencial (un ejercicio por pantalla).
   - Botón de "Validar" para procesar la respuesta y mostrar feedback inmediato.
   - Botón de "Siguiente" para avanzar al próximo ejercicio.
   - Barra de progreso simple que indique cuántos ejercicios quedan.
4. **Persistencia y Feedback:**
   - Guardar cada intento de resolución en `ResultadoEjercicio`.
   - Mostrar un mensaje de retroalimentación explicativa (obtenida del ejercicio o genérica) tras cada respuesta.

## Requerimientos No Funcionales
- **Usabilidad:** Interfaz limpia y centrada en el contenido educativo.
- **Rendimiento:** Carga fluida de los ejercicios mediante peticiones asíncronas (opcional) o recarga de sección.
- **Integridad:** Asegurar que solo estudiantes con temas recomendados accedan a la práctica.

## Criterios de Aceptación
- [ ] El sistema carga ejercicios del tema recomendado para el usuario autenticado.
- [ ] El estudiante puede seleccionar una opción y validarla.
- [ ] El sistema registra si la respuesta fue correcta y el tiempo transcurrido.
- [ ] Se muestra retroalimentación inmediata tras cada validación.
- [ ] Solo se muestran ejercicios de opción múltiple.

## Fuera de Alcance
- Ajuste dinámico de dificultad durante la sesión (se hará en una HU posterior).
- Integración con sistemas de puntos o medallas (HU de gamificación).
- Panel de reportes para el docente.
