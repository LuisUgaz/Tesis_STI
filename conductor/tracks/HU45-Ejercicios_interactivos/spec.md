# Especificación: HU45 - Resolver ejercicios de geometría interactiva en plano dinámico

## Descripción General
Esta historia de usuario consiste en la implementación de un módulo de ejercicios interactivos para el Sistema Tutor Inteligente (STI). Utilizando la librería **JSXGraph**, los estudiantes podrán manipular elementos geométricos (puntos y segmentos) en un plano cartesiano dinámico para resolver problemas relacionados con ángulos y triángulos. El sistema validará estas construcciones mediante propiedades matemáticas derivadas enviadas por AJAX y proporcionará retroalimentación visual superponiendo la solución correcta en caso de error.

## Requerimientos Funcionales

### 1. Modelo de Datos (Extensión de `Pregunta`)
- **Campo `es_interactiva`:** Booleano para distinguir entre ejercicios estáticos y dinámicos.
- **Campo `meta_geometria`:** `JSONField` que almacenará:
  - `tipo_ejercicio`: (ej: "construir_angulo", "propiedad_triangulo", "distancia_segmento").
  - `objetivo`: Valor matemático esperado (ej: grados del ángulo, longitud, coordenadas de meta).
  - `elementos_iniciales`: Configuración de puntos y segmentos que aparecen al cargar el tablero.
  - `tolerancia`: Margen de error aceptable (personalizado por ejercicio).

### 2. Interfaz de Usuario (Frontend)
- **Integración de JSXGraph:** Carga dinámica del tablero solo cuando `es_interactiva` sea `True`.
- **Interactividad:** El estudiante podrá mover puntos móviles definidos en la meta.
- **Validación AJAX:** Al presionar "Validar", el frontend calculará las propiedades geométricas actuales (ej: ángulo entre tres puntos) y las enviará al backend.

### 3. Lógica de Validación (Backend)
- Recepción de datos geométricos vía POST (AJAX).
- Comparación entre el valor calculado por el estudiante y el `objetivo` almacenado en `meta_geometria`.
- Aplicación de la `tolerancia` específica del ejercicio.
- Retorno de un objeto JSON con el resultado, el feedback pedagógico y las coordenadas de la "solución fantasma".

### 4. Retroalimentación Visual
- **Éxito:** Mensaje de confirmación y avance.
- **Error/Parcial:** Superposición de una "solución fantasma" (elementos semi-transparentes) sobre el plano interactivo para mostrar la construcción correcta esperada.

## Requerimientos No Funcionales
- **Compatibilidad:** El sistema debe seguir funcionando correctamente para los ejercicios estáticos existentes (opción múltiple).
- **Rendimiento:** La validación asíncrona no debe exceder los 2 segundos de espera.
- **Usabilidad:** El plano debe ser responsivo y permitir una manipulación fluida de puntos.

## Criterios de Aceptación
1. **Escenario: Visualización de ejercicio interactivo**
   - Dado un ejercicio interactivo configurado.
   - Cuando el estudiante accede a la práctica.
   - Entonces se muestra un plano cartesiano interactivo con los elementos iniciales definidos.
2. **Escenario: Validación con tolerancia**
   - Dado un ejercicio que requiere un ángulo de 90° con tolerancia de 2°.
   - Cuando el estudiante construye un ángulo de 89.5° y valida.
   - Entonces el sistema lo marca como correcto.
3. **Escenario: Retroalimentación con solución fantasma**
   - Dado un ejercicio fallido.
   - Cuando se recibe el resultado del backend.
   - Entonces se dibuja automáticamente sobre el plano la solución correcta en modo "fantasma".
4. **Escenario: Compatibilidad**
   - Dado un ejercicio estático (no interactivo).
   - Cuando el estudiante accede a la práctica.
   - Entonces el sistema muestra la interfaz tradicional sin el plano dinámico.

## Fuera de Alcance
- Generación automática de ejercicios interactivos por IA (Gemini solo dará feedback textual).
- Creación visual de ejercicios desde el Admin (se hará mediante JSON manual por ahora).
- Construcciones complejas con círculos, arcos o cónicas en esta fase.
