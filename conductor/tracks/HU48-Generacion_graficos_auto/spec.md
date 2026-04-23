# Especificación Técnica: HU48 - Generación Automática de Gráficos Geométricos

## 1. Visión General
Esta funcionalidad permite automatizar la creación de representaciones visuales (gráficos) para preguntas de geometría importadas desde documentos (PDF/DOCX) que carecen de imagen. Utiliza IA para traducir enunciados textuales en código Matplotlib, el cual se ejecuta de forma segura para generar archivos SVG vinculados automáticamente a la pregunta.

## 2. Requisitos Funcionales

### 2.1 Motor de Generación Asistida por IA
- **Entrada:** Enunciado de la pregunta geométrica (ej: "Un triángulo con ángulos de 30° y 60°...").
- **Proceso:** 
    - Enviar prompt a Google Gemini solicitando exclusivamente código Python (Matplotlib) para dibujar la figura.
    - El prompt especificará un estilo **"Didáctico Colorido"** (resaltar ángulos/segmentos con colores).
- **Salida:** Bloque de código Python ejecutable.

### 2.2 Entorno de Ejecución Seguro
- El sistema filtrará el código recibido mediante una **"Lista Blanca de Funciones"** permitidas (solo `matplotlib.pyplot`, `numpy`, y funciones de dibujo básicas).
- Se prohíbe el uso de `import os`, `import sys`, `eval`, `exec` (fuera del entorno controlado) o acceso a archivos locales.

### 2.3 Integración en el Flujo de Importación
- **Detección:** Durante la confirmación de importación (`ConfirmarImportacionView`), si una pregunta marcada para importar no tiene imagen, se activa el trigger de generación.
- **Formato:** Los archivos se generarán en formato **SVG** para máxima nitidez.
- **Almacenamiento:** Guardar en `media/ejercicios_imagenes/` con un nombre único vinculado al ejercicio.

### 2.4 Resiliencia y Manejo de Errores
- **Reintento Automático:** Si el código falla al ejecutarse (SyntaxError o RuntimeError), el sistema realizará **un (1) reintento** automático solicitando a la IA una corrección detallando el error obtenido.
- **Fallback Final:** Si el segundo intento falla, la pregunta se importa **sin imagen**, registrando el incidente en los logs pero sin interrumpir el proceso de importación masiva.

## 3. Requisitos No Funcionales
- **Rendimiento:** La generación de cada imagen no debe exceder los 5 segundos.
- **Consistencia:** Mantener la estética visual en todos los gráficos automáticos.

## 4. Criterios de Aceptación
- [ ] El sistema identifica preguntas sin imagen en la vista de confirmación de importación.
- [ ] La IA devuelve código Matplotlib válido basado en la descripción del problema.
- [ ] El código se ejecuta de forma segura y produce un archivo SVG.
- [ ] La imagen SVG se visualiza correctamente en el banco de preguntas y en la práctica del estudiante.
- [ ] El flujo de importación no se detiene ante fallos en la generación de imágenes.

## 5. Fuera de Alcance
- Generación de gráficos 3D o animaciones.
- Edición manual interactiva del gráfico generado.
- Sustitución de imágenes en preguntas que ya poseen una válida.
