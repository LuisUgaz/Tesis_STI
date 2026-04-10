# Plan de Implementación: HU14 - Resolver ejercicios personalizados

## Fase 1: Base de Datos y Modelado
- [x] Task: Crear los modelos `Ejercicio`, `OpcionEjercicio` y `ResultadoEjercicio` en `AppEvaluar/models.py`.
- [x] Task: Registrar los nuevos modelos en `AppEvaluar/admin.py` para permitir la carga de ejercicios por parte de los administradores.
- [x] Task: Generar y aplicar las migraciones de base de datos.
- [x] Task: Conductor - User Manual Verification 'Fase 1: Base de Datos y Modelado' (Protocol in workflow.md)

## Fase 2: Lógica del Backend (Vistas y Endpoints)
- [x] Task: Implementar la vista `iniciar_practica` que seleccione ejercicios según el tema recomendado y el nivel del estudiante.
- [x] Task: Implementar el endpoint `validar_respuesta` que reciba la opción seleccionada, calcule si es correcta, guarde el `ResultadoEjercicio` y retorne feedback.
- [x] Task: Configurar las URLs en `AppEvaluar/urls.py` para la práctica y validación.
- [x] Task: Escribir pruebas unitarias (TDD) para la lógica de selección y validación de respuestas.
- [x] Task: Conductor - User Manual Verification 'Fase 2: Lógica del Backend' (Protocol in workflow.md)

## Fase 3: Interfaz de Usuario (Frontend)
- [x] Task: Crear el template `AppEvaluar/practica_ejercicio.html` con una estructura secuencial (un ejercicio a la vez).
- [x] Task: Implementar la lógica JavaScript para manejar el envío de respuestas vía Fetch/AJAX, mostrar feedback y manejar el botón "Siguiente".
- [x] Task: Diseñar la barra de progreso y estilos de feedback (éxito/error) siguiendo los lineamientos de diseño.
- [x] Task: Conductor - User Manual Verification 'Fase 3: Interfaz de Usuario' (Protocol in workflow.md)

## Fase 4: Integración y Calidad
- [x] Task: Realizar pruebas de integración para asegurar que el flujo Estudiante -> Selección -> Resolución -> Guardado funciona correctamente.
- [x] Task: Verificar que el tiempo transcurrido se calcula y guarda con precisión razonable.
- [x] Task: Conductor - User Manual Verification 'Fase 4: Integración y Calidad' (Protocol in workflow.md)
