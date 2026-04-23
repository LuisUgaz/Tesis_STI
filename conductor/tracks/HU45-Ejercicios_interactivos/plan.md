# Plan de Implementación: HU45 - Resolver ejercicios de geometría interactiva en plano dinámico

Este plan sigue una metodología de **Desarrollo Dirigido por Pruebas (TDD)** y garantiza la compatibilidad con el sistema actual.

## Fase 1: Infraestructura de Datos y Modelos
*Preparación del esquema de base de datos para soportar interactividad.*

- [x] **Task: Actualizar el modelo de datos `Pregunta`**
    - [x] Añadir campos `es_interactiva` (boolean) y `meta_geometria` (JSONField).
    - [x] Registrar los nuevos campos en el sitio administrativo de Django.
    - [x] Escribir prueba de modelo para validar la estructura del JSONField.
- [x] **Task: Migraciones de Base de Datos**
    - [x] Generar y aplicar las migraciones correspondientes en PostgreSQL.
- [ ] **Task: Conductor - User Manual Verification 'Fase 1' (Protocol in workflow.md)**

## Fase 2: Integración Frontend con JSXGraph
*Implementación de la interfaz dinámica y manipulación de elementos.*

- [x] **Task: Configurar JSXGraph en el proyecto**
    - [x] Integrar la librería JSXGraph (vía CDN o local) en los templates base.
    - [x] Crear un componente/script base para la inicialización del tablero (`board`).
- [x] **Task: Lógica de Carga Dinámica del Ejercicio**
    - [x] Escribir pruebas unitarias en JS para la inicialización de puntos y segmentos desde el JSON de la meta.
    - [x] Implementar la función `initInteractiveBoard(meta)` que dibuje los elementos iniciales.
- [x] **Task: Interacción y Captura de Datos**
    - [x] Implementar la captura de coordenadas y cálculo de propiedades (ángulos, distancias) en tiempo real en el frontend.
    - [x] Preparar el payload JSON para el envío AJAX.
- [ ] **Task: Conductor - User Manual Verification 'Fase 2' (Protocol in workflow.md)**

## Fase 3: Motor de Validación Geométrica (Backend)
*Lógica de servidor para comparar la respuesta del estudiante con el objetivo.*

- [x] **Task: Crear servicio de Validación Geométrica**
    - [x] Escribir pruebas unitarias para el servicio de validación (casos de éxito/error con tolerancia).
    - [x] Implementar lógicas para: `validar_angulo`, `validar_distancia`, `validar_triangulo`.
- [x] **Task: Actualizar Vista de Validación Asíncrona**
    - [x] Modificar la vista de entrega de respuestas para detectar si la pregunta es interactiva.
    - [x] Integrar el servicio de validación geométrica en el flujo de respuesta AJAX.
- [ ] **Task: Conductor - User Manual Verification 'Fase 3' (Protocol in workflow.md)**

## Fase 4: Retroalimentación Visual Avanzada (Ghost Overlay)
*Implementación del feedback correctivo visual en el plano.*

- [x] **Task: Lógica de "Solución Fantasma" en Frontend**
    - [x] Desarrollar la función para dibujar elementos semi-transparentes sobre el tablero actual.
    - [x] Integrar esta visualización con la respuesta AJAX de error.
- [x] **Task: Pruebas de Integración de Flujo Completo**
    - [x] Crear pruebas de integración para el flujo: Carga -> Interacción -> Validación -> Feedback Visual.
- [ ] **Task: Conductor - User Manual Verification 'Fase 4' (Protocol in workflow.md)**

## Fase 5: Compatibilidad y Refinamiento
*Asegurar que el sistema siga funcionando íntegramente.*

- [x] **Task: Verificación de Regresión (Ejercicios Estáticos)**
    - [x] Validar que los ejercicios de opción múltiple actuales no se vean afectados.
- [x] **Task: Documentación y Calidad de Código**
    - [x] Completar docstrings y tipado.
    - [x] Verificar cobertura de pruebas (>80%).
- [ ] **Task: Conductor - User Manual Verification 'Fase 5' (Protocol in workflow.md)**
