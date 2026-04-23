# Especificación Técnica: HU46 - Alertas Tempranas de Riesgo de Aprendizaje

## 1. Visión General
Esta funcionalidad permite a los docentes identificar de manera proactiva a estudiantes que presentan patrones de comportamiento improductivos (adivinanza, frustración o estancamiento) en su proceso de aprendizaje de geometría. El sistema analizará las métricas de desempeño y tiempo para generar un índice de riesgo visual en los reportes docentes.

## 2. Requisitos Funcionales

### 2.1 Motor de Detección de Patrones
El sistema debe analizar el historial del estudiante por tema para detectar:
- **Patrón de Adivinanza:** Identificado cuando un estudiante responde incorrectamente en un tiempo inferior al umbral mínimo definido para el ejercicio o tema específico (Default: 5s).
- **Patrón de Frustración:** Identificado cuando el tiempo de respuesta supera el umbral máximo definido (Default: 60s) Y se acumulan múltiples reintentos fallidos en el mismo ejercicio o tema (Min: 3).
- **Patrón de Estancamiento:** Identificado mediante el análisis de la tendencia reciente (últimos 3 intentos), donde el desempeño se mantiene neutro o disminuye a pesar de la actividad continua.

### 2.2 Cálculo del Índice de Riesgo
Se calculará un índice jerárquico basado en la gravedad de los patrones detectados:
- **Riesgo Alto (Rojo):** Presencia de Estancamiento.
- **Riesgo Medio (Amarillo):** Presencia de Frustración o Adivinanza persistente.
- **Riesgo Bajo (Verde):** Sin patrones de riesgo detectados o desempeño positivo consistente.

### 2.3 Integración en Reportes Docentes
- **Backend:** Incorporar el `nivel_riesgo` y `motivo_riesgo` (tooltip) en el objeto JSON de respuesta del reporte de estudiantes.
- **Frontend:** 
    - Mostrar un indicador visual tipo semáforo (círculo de color) en la tabla de reportes por estudiante.
    - Implementar un Tooltip que detalle la razón del riesgo al pasar el cursor sobre el indicador (ej: "Riesgo Alto: Se detectó estancamiento en el tema Triángulos").

## 3. Requisitos No Funcionales
- **Rendimiento:** El cálculo del riesgo debe realizarse de forma eficiente para no degradar el tiempo de carga del reporte docente (< 2s).
- **Consistencia:** Utilizar los datos persistidos en `ResultadoEjercicio` y `MetricasEstudiante`.
- **Trazabilidad:** Las reglas de detección deben ser ajustables mediante configuración (umbrales por tema/ejercicio).

## 4. Criterios de Aceptación
- [ ] El sistema calcula correctamente el patrón de adivinanza basado en umbrales de tiempo por tema.
- [ ] El sistema identifica frustración al cruzar tiempo excesivo y reintentos.
- [ ] El sistema detecta estancamiento analizando la tendencia de los últimos 3 intentos.
- [ ] El nivel de riesgo se incluye en la respuesta JSON del reporte docente.
- [ ] La tabla docente muestra el semáforo con el color correspondiente y un tooltip informativo.

## 5. Fuera de Alcance
- Notificaciones automáticas (emails) por alertas de riesgo.
- Intervenciones automáticas del sistema hacia el estudiante.
- Modelos predictivos avanzados o machine learning en esta fase.
