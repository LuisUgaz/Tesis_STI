# Especificación del Track: HU33 - Registrar Videos Recomendados

## 1. Visión General
Este track tiene como objetivo permitir a los docentes enriquecer el material educativo mediante el registro de videos externos (principalmente de YouTube) vinculados a temas específicos de geometría. El sistema automatizará la obtención de miniaturas para enlaces de YouTube y organizará estos recursos en una nueva sección de gestión de contenidos.

## 2. Requerimientos Funcionales

### 2.1 Gestión de Contenidos (Docente)
- **Acceso Restringido:** Funcionalidad exclusiva para usuarios con rol **Docente**.
- **Módulo de Registro:** Formulario para añadir nuevos videos con los siguientes campos:
    - **Título:** Nombre del video.
    - **Descripción:** Breve resumen del contenido.
    - **Tema Asociado:** Selección del tema de geometría (Relación con modelo `Tema`).
    - **Enlace Externo:** URL del video (YouTube).
- **Automatización de Miniaturas:** El sistema detectará si el enlace es de YouTube y extraerá automáticamente el ID del video para generar la URL de la miniatura oficial.
- **Sección Dedicada:** Los videos se administrarán desde una nueva vista de "Gestión de Contenidos" accesible para el docente.

### 2.2 Consumo Estudiantil (Integración)
- Los videos registrados deben aparecer automáticamente en la sección de "Videos Recomendados" del estudiante cuando coincidan con su tema recomendado.

## 3. Requerimientos Técnicos
- **Backend:** Vista `VideoTemaCreateView` en `AppTutoria/views.py`.
- **Lógica de Validación:** Implementar utilidad para validar y parsear URLs de YouTube.
- **Modelos:** Reutilizar o ajustar el modelo `VideoTema` existente en `AppTutoria`.
- **Frontend:** Template `AppTutoria/video_registro_form.html` siguiendo el estilo visual del panel docente.

## 4. Criterios de Aceptación
- **Escenario: Registro exitoso:** El docente ingresa un título, selecciona "Triángulos", pega un enlace de YouTube válido y guarda. El video aparece con su miniatura en la lista de gestión y para los estudiantes.
- **Escenario: Validación de URL:** El sistema rechaza enlaces que no tengan un formato válido de YouTube o que estén vacíos.
- **Escenario: Persistencia:** Los datos del video (incluyendo la referencia al tema) se guardan correctamente en PostgreSQL.

## 5. Fuera de Alcance
- Edición compleja de metadatos de video una vez registrados.
- Analítica detallada de visualizaciones (fuera de lo ya implementado).
- Carga de archivos de video locales (solo enlaces externos).
