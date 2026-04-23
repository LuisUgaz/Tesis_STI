# Plan de Implementación - HU47: Repetición Espaciada

## Fase 1: Infraestructura de Datos (Modelos) [checkpoint: verified]
- [x] **Task: Crear modelo `RepasoProgramado` en `AppEvaluar/models.py`**
    - [x] Campos: `estudiante`, `tema`, `fecha_proximo_repaso`, `intervalo`, `factor_facilidad`, `estado`.
- [x] **Task: Generar y aplicar migraciones**
    - [x] `python manage.py makemigrations AppEvaluar`
    - [x] `python manage.py migrate`
- [x] **Task: Conductor - User Manual Verification 'Fase 1: Infraestructura' (Protocol in workflow.md)**

## Fase 2: Lógica de Repetición Espaciada (TDD) [checkpoint: verified]
- [x] **Task: Crear `AppEvaluar/services_spaced_repetition.py`**
    - [x] Función `calcular_siguiente_repaso(intervalo_actual, ef_actual, es_exito)`.
- [x] **Task: Escribir pruebas unitarias para la lógica SM-2**
    - [x] Test: Aumento de intervalo tras acierto.
    - [x] Test: Reducción de intervalo y EF tras fallo (Penalización Suave).
- [x] **Task: Implementar lógica SM-2 en el servicio**
- [x] **Task: Conductor - User Manual Verification 'Fase 2: Lógica de Repetición' (Protocol in workflow.md)**

## Fase 3: Automatización de Repasos (Trigger) [checkpoint: verified]
- [x] **Task: Crear señal o hook para detectar dominio de tema**
    - [x] Verificar umbral: Precisión > 90% y Ejercicios > 10.
    - [x] Crear `RepasoProgramado` inicial (1 día) al cumplir el umbral.
- [x] **Task: Escribir pruebas unitarias para el trigger de dominio**
- [x] **Task: Conductor - User Manual Verification 'Fase 3: Automatización' (Protocol in workflow.md)**

## Fase 4: Integración en Motor de Recomendación [checkpoint: verified]
- [x] **Task: Actualizar `calcular_recomendacion` en `AppEvaluar/services.py`**
    - [x] Consultar repasos vencidos (`fecha_proximo_repaso <= hoy`).
    - [x] Priorizar el repaso más antiguo sobre debilidades.
- [x] **Task: Escribir pruebas de integración para la recomendación**
- [x] **Task: Conductor - User Manual Verification 'Fase 4: Integración' (Protocol in workflow.md)**

## Fase 5: Ciclo de Actualización [checkpoint: verified]
- [x] **Task: Actualizar `RepasoProgramado` tras resolución de ejercicio**
    - [x] Si el tema recomendado era un repaso, actualizar su fecha e intervalo según el resultado.
- [x] **Task: Escribir pruebas unitarias para la actualización del estado del repaso**
- [x] **Task: Conductor - User Manual Verification 'Fase 5: Ciclo de Actualización' (Protocol in workflow.md)**
