# Plan de Implementación - HU48: Generación de Gráficos con IA

## Fase 1: Servicio de Generación de Código (Backend) [checkpoint: verified]
- [x] **Task: Crear `AppEvaluar/services_ia_graphics.py`**
    - [x] Implementar `generar_codigo_grafico(enunciado, error_previo=None)` para llamar a Gemini.
    - [x] Definir el prompt especializado (estilo didáctico, salida código puro).
- [x] **Task: Implementar validador de seguridad (Sandbox Básico)**
    - [x] Función `validar_codigo_seguro(codigo)` que verifique palabras prohibidas e imports permitidos.
- [x] **Task: Escribir pruebas unitarias para la generación de código**
    - [x] Verificar que el prompt genera código Matplotlib coherente.
    - [x] Validar que el sandbox bloquee código malicioso.
- [x] **Task: Conductor - User Manual Verification 'Fase 1: Generación Código' (Protocol in workflow.md)**

## Fase 2: Ejecución y Almacenamiento [checkpoint: verified]
- [x] **Task: Implementar `ejecutar_grafico_y_guardar(codigo, ejercicio_id)`**
    - [x] Usar `io.BytesIO` para capturar el SVG de Matplotlib.
    - [x] Guardar en `FileField` del ejercicio.
- [x] **Task: Manejo de reintentos y fallback**
    - [x] Lógica de control en `procesar_imagen_automatica(enunciado, ejercicio)`.
- [x] **Task: Escribir pruebas unitarias para la ejecución**
    - [x] Mock de Matplotlib para verificar guardado de SVG.
    - [x] Test de flujo de reintento ante código erróneo.
- [x] **Task: Conductor - User Manual Verification 'Fase 2: Ejecución y Guardado' (Protocol in workflow.md)**

## Fase 3: Integración en Importación [checkpoint: verified]
- [x] **Task: Modificar `ConfirmarImportacionView` en `AppEvaluar/views.py`**
    - [x] Identificar ejercicios sin imagen y llamar al servicio de IA.
- [x] **Task: Actualizar template de confirmación (si es necesario)**
    - [x] Mostrar un indicador de "Generando imagen..." o similar.
- [x] **Task: Escribir pruebas de integración para la importación**
    - [x] Simular importación de PDF/texto y verificar generación de imagen.
- [x] **Task: Conductor - User Manual Verification 'Fase 3: Integración Importación' (Protocol in workflow.md)**

## Fase 4: Validación y Cobertura [checkpoint: verified]
- [x] **Task: Ejecutar suite de pruebas completa**
- [x] **Task: Conductor - User Manual Verification 'Fase 4: Validación Final' (Protocol in workflow.md)**
