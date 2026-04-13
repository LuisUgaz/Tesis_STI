# Plan de Implementación: HU33 - Registrar Videos Recomendados

## Fase 1: Pruebas Iniciales y Estructura (Red Phase)
- [x] Task: Crear pruebas unitarias para el registro de videos.
    - [x] Escribir tests en `AppTutoria/tests_video_registration.py` para validar:
        - Registro correcto con URL de YouTube válida.
        - Rechazo de URLs inválidas o formatos no soportados.
        - Extracción automática de la miniatura.
        - Asociación obligatoria a un Tema.
- [x] Task: Ejecutar pruebas y confirmar que fallan (Fase Roja).
- [x] Task: Conductor - User Manual Verification 'Pruebas Iniciales' (Protocolo en workflow.md)

## Fase 2: Implementación de Lógica y Vistas (Green Phase)
- [x] Task: Actualizar o validar el modelo `VideoTema` en `AppTutoria/models.py`.
    - [x] Asegurar campos: `titulo`, `descripcion`, `url_video`, `url_miniatura`, `tema` (FK).
- [x] Task: Desarrollar utilidad de procesamiento de YouTube.
    - [x] Implementar función para extraer el ID de video y generar la URL de la miniatura.
- [x] Task: Implementar la vista de creación `VideoTemaCreateView`.
    - [x] Crear formulario `VideoTemaForm` con validaciones personalizadas de URL.
    - [x] Implementar la vista con restricciones de rol (Docente).
    - [x] Registrar la nueva ruta en `AppTutoria/urls.py`.
- [x] Task: Ejecutar pruebas y confirmar que pasan (Fase Verde).
- [x] Task: Conductor - User Manual Verification 'Implementación de Lógica' (Protocolo en workflow.md)

## Fase 3: Interfaz de Usuario e Integración
- [x] Task: Diseñar las interfaces de gestión de videos.
    - [x] Crear el template `AppTutoria/video_registro_form.html` con estilo moderno.
    - [x] Crear vista de listado `VideoTemaListView` para la administración del docente.
    - [x] Añadir sección de "Gestión de Contenidos" en el menú lateral o superior para el Docente.
- [x] Task: Verificación de integración con la vista del Estudiante.
    - [x] Confirmar que los nuevos videos aparecen en la sección de recomendaciones del alumno.
- [x] Task: Conductor - User Manual Verification 'Interfaz e Integración' (Protocolo en workflow.md)
