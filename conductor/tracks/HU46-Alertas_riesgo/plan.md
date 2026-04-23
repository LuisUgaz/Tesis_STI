# Plan de Implementación - HU46: Alertas Tempranas de Riesgo

## Fase 1: Lógica de Detección de Riesgos (Backend & TDD)
- [x] **Task: Definir constantes de umbrales en `AppEvaluar/services_metrics.py`**
    - [x] Definir `TIEMPO_MIN_ADIVINANZA = 5` (segundos).
    - [x] Definir `TIEMPO_MAX_FRUSTRACION = 60` (segundos).
    - [x] Definir `MIN_REINTENTOS_FRUSTRACION = 3`.
- [x] **Task: Crear pruebas unitarias en `AppEvaluar/tests_risk_alerts.py`**
    - [x] Test para detección de Adivinanza (Tiempo < 5s + Incorrecto).
    - [x] Test para detección de Frustración (Tiempo > 60s + 3+ reintentos).
    - [x] Test para detección de Estancamiento (Tendencia negativa en últimos 3 intentos).
    - [x] Test para el cálculo del semáforo (Jerarquía: Rojo > Amarillo > Verde).
- [x] **Task: Implementar función `calcular_riesgo_estudiante(usuario, tema_id=None)`**
    - [x] Analizar `ResultadoEjercicio` filtrados por usuario y tema.
    - [x] Aplicar lógica de patrones definidos.
    - [x] Retornar diccionario con `nivel` ('bajo', 'medio', 'alto'), `color` ('green', 'yellow', 'red') y `mensaje`.
- [x] **Task: Conductor - User Manual Verification 'Fase 1: Lógica de Detección' (Protocol in workflow.md)**

## Fase 2: Integración en API de Reportes
- [x] **Task: Actualizar `ReportesDataJSONView` en `AppEvaluar/views.py`**
    - [x] Importar la nueva función de riesgo.
    - [x] Iterar sobre los estudiantes y adjuntar los datos de riesgo a la respuesta JSON.
- [x] **Task: Actualizar `tests_teacher_reports.py`**
    - [x] Verificar que el JSON ahora incluye los campos `nivel_riesgo` y `motivo_riesgo`.
- [x] **Task: Conductor - User Manual Verification 'Fase 2: Integración API' (Protocol in workflow.md)**

## Fase 3: Interfaz de Usuario (Semáforo de Riesgo)
- [x] **Task: Modificar `reportes_docente.html`**
    - [x] Agregar columna "Riesgo" en la tabla de estudiantes.
    - [x] Implementar el indicador visual (círculo de color) con Bootstrap y CSS.
    - [x] Integrar Tooltips de Bootstrap para mostrar el motivo del riesgo.
    - [x] Actualizar la lógica de JavaScript para pintar el semáforo dinámicamente al filtrar.
- [x] **Task: Conductor - User Manual Verification 'Fase 3: Interfaz de Usuario' (Protocol in workflow.md)**

## Fase 4: Validación y Cobertura
- [x] **Task: Ejecutar suite de pruebas completa**
    - [x] Asegurar que el reporte de cobertura supere el 80% en los archivos modificados.
- [x] **Task: Conductor - User Manual Verification 'Fase 4: Validación Final' (Protocol in workflow.md)**
