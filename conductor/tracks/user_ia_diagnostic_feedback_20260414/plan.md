# Plan de Implementación: HU40 - Generar retroalimentación inteligente al finalizar el examen diagnóstico

Este plan sigue la metodología TDD y se divide en fases para asegurar una integración fluida de la IA y una experiencia de usuario optimizada.

## Fase 1: Interacción de Envío y Experiencia de Usuario (UI/UX)
- [x] Task: Crear el componente de **Modal de Confirmación** en la plantilla `AppEvaluar/templates/AppEvaluar/rendir_examen.html`.
- [x] Task: Implementar el **Overlay Bloqueante** con spinner de carga activado por JavaScript al confirmar el envío.
- [x] Task: Actualizar el formulario de envío en `rendir_examen.html` para integrarse con el modal y el overlay.
- [x] Task: Conductor - User Manual Verification 'Fase 1: Interacción de Envío y UX' (Protocol in workflow.md)

## Fase 2: Infraestructura Backend para IA (Service & Endpoint)
- [x] Task: Crear pruebas unitarias para el servicio de orquestación de IA en `AppEvaluar/tests_ia_feedback.py` (Red Phase).
- [x] Task: Implementar el servicio `obtener_feedback_ia` en `AppEvaluar/services.py` que construya el prompt multimodal y se comunique con Gemini 1.5 Flash (Green Phase).
- [x] Task: Crear la vista `IAFeedbackView` en `AppEvaluar/views.py` que actúe como endpoint para las peticiones AJAX.
- [x] Task: Configurar la URL para el endpoint de IA en `AppEvaluar/urls.py`.
- [x] Task: Verificar que el endpoint esté protegido por login y valide que el usuario sea el dueño del examen.
- [x] Task: Conductor - User Manual Verification 'Fase 2: Infraestructura Backend para IA' (Protocol in workflow.md)

## Fase 3: Integración Frontend y Carga Diferida (AJAX)
- [x] Task: Crear pruebas funcionales para la vista de resultados que verifiquen la estructura de carga diferida (Red Phase).
- [x] Task: Actualizar la plantilla `AppEvaluar/templates/AppEvaluar/resultados.html` para incluir los contenedores de retroalimentación IA dentro de un componente **Colapsable (Acordeón)**.
- [x] Task: Implementar el script JavaScript en `resultados.html` que realice las llamadas AJAX al cargar la página y pueble los acordeones con el contenido de la IA.
- [x] Task: Implementar el manejo visual de errores (fallback) en el script frontend si la petición falla.
- [x] Task: Conductor - User Manual Verification 'Fase 3: Integración Frontend y Carga Diferida' (Protocol in workflow.md)

## Fase 4: Refactorización y Cobertura
- [x] Task: Refactorizar el prompt de la IA y el orquestador backend para optimizar tiempos de respuesta.
- [x] Task: Realizar pruebas integrales de extremo a extremo (End-to-End) simulando un envío de examen completo.
- [x] Task: Verificar cobertura de pruebas (>80%) para los nuevos módulos de IA.
- [x] Task: Conductor - User Manual Verification 'Fase 4: Refactorización y Cobertura' (Protocol in workflow.md)
