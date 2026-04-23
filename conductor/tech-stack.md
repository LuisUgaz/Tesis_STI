# Tech Stack (Tesis STI)

Esta es la pila tecnológica oficial seleccionada para el desarrollo y despliegue del Sistema Tutor Inteligente Adaptativo.

## 1. Lenguaje y Backend
- **Python:** Lenguaje principal por su potencia en lógica de negocio y procesamiento de datos.
- **Django:** Framework backend por su robustez, sistema de autenticación integrado y capacidad de gestión de base de datos relacional.
- **Django Channels:** Soporte para WebSockets para actualizaciones en tiempo real (ranking, progreso dinámico).

## 2. Base de Datos
- **PostgreSQL:** Base de datos relacional elegida por su capacidad de mantener integridad referencial y su escalabilidad en sistemas académicos.

## 3. Frontend
- **HTML5 & CSS3:** Maquetación y estilos modernos.
- **JavaScript (Vanilla):** Lógica del lado del cliente para interactividad en ejercicios y gamificación.
- **Chart.js:** Librería para la visualización de métricas y reportes analíticos mediante gráficos interactivos.
- **JSXGraph (HU45):** Librería especializada para la visualización y manipulación de geometría dinámica en el navegador.
- **SVG (Scalable Vector Graphics):** Para la visualización de figuras geométricas nítidas y escalables.
- **SMTP / Django Mail:** Motor de mensajería para el envío de consultas de estudiantes directamente al correo electrónico de los docentes.

## 4. Inteligencia Artificial y Ciencia de Datos
- **Google Gemini AI (API):** Utilizado para la generación de retroalimentación pedagógica inteligente basada en el contexto del estudiante y errores específicos.
- **Scikit-learn:** Librería de Machine Learning utilizada para implementar el clasificador SVM que resuelve empates técnicos en las recomendaciones adaptativas.
- **NumPy:** Soporte para el procesamiento de vectores de características y cálculos matriciales requeridos por los modelos de IA.

## 5. Otros Servicios y Herramientas
- **WebSockets:** Para comunicación bidireccional en tiempo real entre el servidor y el cliente.
- **Arquitectura:** Monolito modular con Django Apps (`AppEvaluar`, `AppGestionUsuario`, `AppTutoria`).
- **Plataforma:** Aplicación web accesible desde cualquier navegador moderno (Responsive).
