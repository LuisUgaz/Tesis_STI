# Specification: HU08 - Visualizar tema recomendado

## Overview
Esta historia de usuario se centra en la presentación visual de la recomendación generada por el sistema. El objetivo es que el estudiante pueda identificar rápidamente el tema que debe reforzar al acceder a la lista de temas geométricos, facilitando su ruta de aprendizaje personalizada.

## Functional Requirements
1.  **Consulta de Recomendación:** El sistema debe consultar la recomendación persistida en la base de datos para el estudiante actual.
2.  **Presentación en Interfaz (Lista de Temas):**
    - Al acceder a la lista de temas, el sistema identificará cuál es el tema recomendado.
    - Se aplicará una diferenciación visual mediante etiquetas (Badge "Recomendado para ti") y se posicionará el tema al principio de la lista.
3.  **Estado Sin Recomendación:**
    - Si el estudiante no ha realizado el examen diagnóstico o no tiene una recomendación procesada, el sistema mostrará un mensaje informativo invitándolo a rendir la evaluación.
4.  **Optimización de Render:** No se recalculará la lógica de recomendación en cada carga de página; se utilizará el dato previamente persistido.

## Non-Functional Requirements
1.  **Separación de Preocupaciones:** Mantener la lógica de negocio en servicios y la lógica de presentación en las vistas y templates de Django.
2.  **Consistencia Visual:** Seguir los principios de diseño de la plataforma para el resaltado de elementos (uso de CSS/HTML consistente).
3.  **Rendimiento:** La consulta de la recomendación debe ser eficiente (uso de `select_related` o índices si es necesario).

## Acceptance Criteria
- **Escenario: Visualización exitosa de la recomendación**
    - **Given** que el sistema ya procesó y persistió la recomendación del diagnóstico para el estudiante.
    - **When** el estudiante accede al menú de lista de temas.
    - **Then** el sistema debe mostrar el tema recomendado con una etiqueta visible.
    - **And** el tema recomendado debe aparecer en la primera posición de la lista.
- **Escenario: Ausencia de recomendación**
    - **Given** que el estudiante no tiene una recomendación previa.
    - **When** el estudiante accede al menú de lista de temas.
    - **Then** el sistema debe mostrar un mensaje invitándolo a realizar el examen diagnóstico.

## Out of Scope
- Apertura automática del tema recomendado al ingresar a la plataforma.
- Asignación automática de ejercicios específicos (se limita a resaltar el tema).
- Comparativas avanzadas de progreso entre diferentes temas.
