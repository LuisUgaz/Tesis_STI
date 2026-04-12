# Initial Concept
Contexto general del proyecto:
El proyecto de tesis consiste en el desarrollo de un Sistema Tutor Inteligente Adaptativo orientado a apoyar el aprendizaje de problemas geomÃ©tricos en estudiantes de segundo de secundaria del colegio Pedro Abel Labarthe Durand. El propÃ³sito central del sistema es fortalecer el aprendizaje en geometrÃ­a mediante una plataforma web que personaliza ejercicios, brinda retroalimentaciÃ³n inmediata y registra el progreso del estudiante.

La problemÃ¡tica parte de que, en el nivel de secundaria, y particularmente en segundo grado, existen dificultades en la comprensiÃ³n de nociones bÃ¡sicas de geometrÃ­a y en la resoluciÃ³n de problemas vinculados a esta Ã¡rea. En la documentaciÃ³n se seÃ±ala que este contexto requiere apoyos mÃ¡s eficaces, ya que los estudiantes presentan vacÃ­os de aprendizaje que afectan su desempeÃ±o y hacen necesario un reforzamiento mÃ¡s especÃ­fico y personalizado. AdemÃ¡s, se menciona que en el colegio se reportan necesidades de recuperaciÃ³n acadÃ©mica, lo que refuerza la necesidad de una soluciÃ³n que acompaÃ±e al estudiante de manera mÃ¡s individualizada.

Frente a esta situaciÃ³n, la propuesta plantea una soluciÃ³n tecnolÃ³gica en forma de tutor inteligente accesible desde navegador, capaz de adaptar el contenido segÃºn el rendimiento del estudiante. El sistema incorpora un examen diagnÃ³stico, un mecanismo de recomendaciÃ³n de temas, ejercicios por tema y nivel, retroalimentaciÃ³n inmediata, material teÃ³rico, videos de apoyo, seguimiento del progreso, gamificaciÃ³n y paneles de reportes para docentes. La idea es que el estudiante no reciba una secuencia fija de ejercicios, sino una experiencia mÃ¡s ajustada a sus necesidades de aprendizaje.

Desde el enfoque pedagÃ³gico, el proyecto se apoya en principios como la progresiÃ³n por dominio, la evaluaciÃ³n formativa con retroalimentaciÃ³n inmediata, la prÃ¡ctica guiada, la metacogniciÃ³n y el uso de recursos visuales o dinÃ¡micos para fortalecer el razonamiento espacial en geometrÃ­a. La tesis sostiene que esta combinaciÃ³n busca atacar causas frecuentes del problema, como vacÃ­os conceptuales, dÃ©bil razonamiento espacial y baja autorregulaciÃ³n en el aprendizaje.

En cuanto a la implementaciÃ³n tecnolÃ³gica, la aplicaciÃ³n estÃ¡ concebida como una plataforma web basada en Django, donde el backend administra la autenticaciÃ³n, la lÃ³gica del negocio, los roles de usuario, el procesamiento del progreso, la gamificaciÃ³n y la interacciÃ³n con la base de datos. El frontend se apoya en HTML, CSS y JavaScript, mostrando mÃ³dulos como ejercicios, exÃ¡menes, temas, videos, perfil del estudiante y reportes. La documentaciÃ³n tambiÃ©n menciona una arquitectura con servicios web y posibilidad de actualizaciÃ³n en tiempo real mediante Django Channels y WebSockets, especialmente para ranking, notificaciones o avances dinÃ¡micos.

La base de datos propuesta para el proyecto es PostgreSQL, utilizada para almacenar usuarios, ejercicios, resultados, logros, estadÃ­sticas y demÃ¡s elementos del sistema. La tesis remarca que su estructura relacional permite mantener integridad referencial y consultas eficientes, lo cual es importante porque el sistema maneja informaciÃ³n acadÃ©mica, seguimiento del progreso y elementos de gamificaciÃ³n.

AdemÃ¡s, el sistema contempla distintos tipos de usuario, como estudiantes, docentes y administrador. El estudiante interactÃºa con el examen diagnÃ³stico, los temas recomendados, los ejercicios, la retroalimentaciÃ³n y su perfil gamificado. El docente puede revisar reportes, monitorear el progreso y gestionar ciertos contenidos. El administrador se encarga de la gestiÃ³n general del sistema.

En tÃ©rminos funcionales ya evidenciados en la documentaciÃ³n, el sistema cuenta con mÃ³dulos de temas como triÃ¡ngulos, Ã¡ngulos y segmentos, ejercicios por tema, feedback inmediato, seguimiento del progreso, videos de apoyo, gamificaciÃ³n con puntos, niveles e insignias, y gestiÃ³n de contenidos. La documentaciÃ³n de ejecuciÃ³n indica que la mayor parte de los requisitos funcionales ya fueron implementados y probados, quedando pendiente principalmente la exportaciÃ³n de reportes a formatos externos.

2. Contexto tÃ©cnico del proyecto:
Proyecto: Sistema Tutor Inteligente Adaptativo para el aprendizaje de problemas geomÃ©tricos en estudiantes de segundo de secundaria del colegio Pedro Abel Labarthe Durand.

Enfoque funcional del sistema:
AutenticaciÃ³n de usuarios
Examen diagnÃ³stico
RecomendaciÃ³n de temas segÃºn desempeÃ±o
Ejercicios por tema y nivel
RetroalimentaciÃ³n inmediata
Material teÃ³rico y videos de apoyo
Registro de progreso
Perfil del estudiante con puntos, niveles e insignias
Reportes para docentes
GestiÃ³n de contenidos por roles

Stack tecnolÃ³gico:
Lenguaje principal: Python
Framework backend: Django
Base de datos: PostgreSQL
Frontend: HTML, CSS, JavaScript
Posible soporte en tiempo real: Django Channels + WebSockets

Base de datos PostgreSQL:
NAME = Base_Tesis
USER = postgres
PASSWORD = 1234
HOST = 127.0.0.1
PORT = 5432

Contexto de arquitectura:
AplicaciÃ³n web accesible desde navegador
Backend Django para lÃ³gica de negocio, autenticaciÃ³n y gestiÃ³n de roles
PostgreSQL como base de datos relacional
Frontend web para interacciÃ³n del estudiante y docente
Sistema orientado a aprendizaje adaptativo y gamificaciÃ³n

Roles principales:
Estudiante
Docente
Administrador

MÃ³dulos principales esperados:
Login / autenticaciÃ³n
Examen diagnÃ³stico
Temas de geometrÃ­a
Ejercicios y exÃ¡menes
RetroalimentaciÃ³n
Videos y teorÃ­a
Perfil del estudiante
Reportes
GestiÃ³n de preguntas y contenidos


OBJETIVO GENERAL:
Desarrollar un sistema tutor inteligente para apoyar el proceso de aprendizaje en el Ã¡rea de geometrÃ­a de los alumnos de segundo de secundaria del colegio nacional Pedro Abel Labarthe Durand.

OBJETIVOS ESPECÃFICOS:
Evaluar diferentes algoritmos de recomendaciÃ³n, a partir de los resultados del examen diagnÃ³stico del estudiante, con el fin de seleccionar el mÃ¡s adecuado para contextualizar las variables que requiera el algoritmo con la realidad de estudio y personalizar los ejercicios de apoyo.
Incorporar un modelo educativo contextualizado, adaptado a las necesidades del aprendizaje en geometrÃ­a, de modo que el software integre un enfoque pedagÃ³gico que respalde el proceso de aprendizaje y las interfaces diseÃ±adas.
Integrar el algoritmo seleccionado con el modelo a la aplicaciÃ³n web que permita la interacciÃ³n humana y computador mÃ¡s Ã¡gil.
Determinar el nivel de calidad de software en cuanto a su funcionalidad, con el propÃ³sito de validar su funcionamiento en tÃ©rminos de satisfacciÃ³n de los usuarios.

Requerimientos funcionales:

El sistema debe permitir el registro de usuarios.
El sistema debe permitir el inicio de sesiÃ³n de estudiantes, docentes y administrador.
El sistema debe gestionar perfiles diferenciados segÃºn rol.
El sistema debe aplicar un examen diagnÃ³stico de geometrÃ­a.
El sistema debe registrar los resultados del examen diagnÃ³stico.
El sistema debe procesar los resultados con un algoritmo de recomendaciÃ³n.
El sistema debe recomendar el tema a reforzar segÃºn el desempeÃ±o del estudiante.
El sistema debe asignar ejercicios personalizados segÃºn el rendimiento del estudiante.
El sistema debe ajustar la dificultad de los ejercicios de forma adaptativa.
El sistema debe permitir resolver ejercicios dentro del entorno web.
El sistema debe brindar retroalimentaciÃ³n inmediata a cada respuesta.
El sistema debe mostrar apoyo teÃ³rico por tema.
El sistema debe mostrar videos recomendados de apoyo.
El sistema debe registrar el progreso del estudiante.
El sistema debe almacenar y consultar el historial de resultados y logros.
El sistema debe calcular mÃ©tricas de desempeÃ±o acadÃ©mico.
El sistema debe otorgar puntos por actividades completadas.
El sistema debe permitir al estudiante subir de nivel segÃºn su rendimiento.
El sistema debe otorgar insignias automÃ¡ticas por metas o constancia.
El sistema debe mostrar al estudiante su perfil con progreso, puntos, niveles e insignias.
El sistema debe generar reportes de progreso para docentes.
El sistema debe permitir filtrar reportes por estudiante, fecha u otros criterios.
El sistema debe permitir administrar el banco de problemas geomÃ©tricos.
El sistema debe permitir registrar, editar y eliminar preguntas y respuestas del banco.
El sistema debe permitir administrar videos recomendados.
El sistema debe permitir al docente visualizar estadÃ­sticas por estudiante y por aula.
El sistema debe permitir la gestiÃ³n administrativa de usuarios, contenidos e insignias.
El sistema debe permitir el envÃ­o de consultas del estudiante al docente mediante el mÃ³dulo â€œContÃ¡ctanosâ€.

Requerimientos no funcionales:

El sistema debe ser accesible desde navegadores web comunes.
El sistema debe ser multiplataforma y funcionar en PC, laptop, tablet y mÃ³viles compatibles.
El sistema debe autenticar usuarios con credenciales seguras.
El sistema debe cifrar los datos sensibles y las contraseÃ±as.
El sistema debe usar comunicaciÃ³n segura mediante HTTPS/TLS.
El sistema debe responder en menos de 2 segundos en los procesos principales.
El sistema debe estar disponible al menos el 95 % del tiempo escolar.
El sistema debe soportar al menos 200 usuarios concurrentes en su primera versiÃ³n.
El sistema debe ser mantenible, modular y documentado.
La interfaz debe ser intuitiva y motivadora sin distraer del aprendizaje.
El sistema debe ser compatible con HTML5, CSS3, JavaScript y WebSockets en navegadores soportados.
El sistema debe funcionar con una resoluciÃ³n mÃ­nima de 1280x720.
El sistema debe operar sin instalaciÃ³n pesada, ejecutÃ¡ndose desde navegador.
El sistema debe preservar la integridad de los datos mediante una base de datos relacional.
El sistema debe permitir escalabilidad e integraciÃ³n mediante backend web/API.
El sistema debe ofrecer usabilidad aceptable validada con pruebas o encuestas de usuarios.

Regla Importante:
Toda la documentaciÃ³n, preguntas y acciones que se realicen debe estar en espaÃ±ol
No realizar ningÃºn commit o git, los cambios se guardaran de forma manual

# Sistema Tutor Inteligente Adaptativo para Geometría (Tesis STI)

## Visión del Producto
Desarrollar una plataforma web educativa basada en un Sistema Tutor Inteligente (STI) que personalice el aprendizaje de la geometría para estudiantes de segundo de secundaria del colegio Pedro Abel Labarthe Durand. El sistema busca fortalecer la comprensión conceptual y la resolución de problemas mediante la adaptación dinámica de contenidos, retroalimentación inmediata y elementos de gamificación.

## Objetivos Estratégicos
- **Fortalecimiento del aprendizaje:** Superar los vacíos conceptuales en geometría mediante una práctica personalizada y guiada.
- **Adaptabilidad Basada en Desempeño:** Implementar un algoritmo de recomendación basado en reglas heurísticas personalizadas que asigne ejercicios según el nivel real del estudiante detectado en un examen diagnóstico.
- **Motivación y Gamificación:** Incrementar el compromiso del estudiante mediante un sistema de puntos, medallas y niveles que reflejen su crecimiento académico.
- **Monitoreo Docente:** Proveer herramientas de seguimiento y reportes para que los docentes identifiquen necesidades específicas de sus alumnos.

## Roles de Usuario
- **Estudiante (2do Secundaria):** Realiza diagnósticos, accede a recomendaciones de temas, resuelve ejercicios interactivos y visualiza su progreso gamificado.
- **Docente (Colegio Labarthe):** Monitorea el progreso del aula, visualiza estadísticas detalladas y gestiona contenidos educativos.
- **Administrador del Sistema:** Encargado de la gestión general de usuarios, banco de preguntas, contenidos multimedia e insignias.

## Funcionalidades Core
- **Examen Diagnóstico (HU05):** Evaluación inicial implementada con gestión de preguntas (opción múltiple/texto) vía Admin, temporizador global y cálculo de resultados por tema.
- **Persistencia de Resultados (HU06):** Registro formal del desempeño diagnóstico con cálculo de puntaje automatizado (escala 100), validación de intento único y almacenamiento histórico para alimentar los algoritmos de recomendación.
- **Algoritmo de Recomendación (HU07):** Lógica de procesamiento de resultados que identifica el tema con mayor necesidad de refuerzo mediante un algoritmo de pesos por desempeño, permitiendo una personalización precisa del aprendizaje.
- **Visualización de Temas Recomendados (HU08):** Interfaz personalizada que resalta el tema sugerido para el estudiante en el menú de tutoría, reordenando los contenidos para priorizar el refuerzo identificado.
- **Gestión Dinámica de Temas (HU09):** Sistema de persistencia basado en base de datos para los temas de geometría, con control de acceso estricto por rol (Estudiante) y visualización adaptativa.
- **Acceso a Contenido de Tema (HU10):** Visualización detallada de material de aprendizaje (HTML enriquecido y PDF) con navegación amigable por slugs y control de acceso basado en recomendaciones previas, asegurando un aprendizaje dirigido.
- **Visualización de Marco Teórico (HU11):** Interfaz de detalle expandida con menú lateral (Sidebar) que permite navegar entre resumen del tema, marco teórico detallado y marcadores para actividades futuras, organizando el estudio de forma jerárquica.
- **Visualización de Videos Recomendados (HU12):** Nueva sección independiente con grilla de tarjetas moderna que permite al estudiante acceder a videos educativos (locales) específicos para reforzar el tema recomendado, con reproductor modal integrado.
- **Seguimiento de Visualización de Videos (HU13):** Registro automatizado que contabiliza cuántas veces un estudiante termina de ver un recurso audiovisual, permitiendo un monitoreo administrativo del uso de materiales por grado y sección.
- **Resolución de Ejercicios Personalizados (HU14):** Sistema de práctica interactiva que selecciona ejercicios de opción múltiple basados en el tema recomendado para el estudiante, con visualización secuencial, barra de progreso y retroalimentación inmediata asíncrona.
- **Ajuste de Dificultad Adaptativa (HU15):** Motor de personalización que asigna un nivel inicial (Básico, Intermedio, Avanzado) tras el diagnóstico y recalcula dinámicamente el desafío tras cada sesión de práctica, asegurando que los ejercicios cargados coincidan con el rendimiento actual del estudiante.
- **Retroalimentación Inmediata (HU16):** Sistema de feedback detallado tras cada respuesta que combina la explicación específica de la opción seleccionada con un fundamento teórico general (Feedback Mixto), reforzado visualmente con iconografía de estado y tarjetas de ayuda.
- **Registro de Progreso de Aprendizaje (HU17):** Sistema de persistencia centralizado que captura y almacena automÃ¡ticamente cada interacciÃ³n educativa (ejercicios, videos, teorÃ­a, exÃ¡menes) del estudiante, registrando el tema, la fecha y su periodo acadÃ©mico (grado/secciÃ³n) actual para construir un historial de avance detallado.
- **Consultar Historial de Resultados (HU18):** Interfaz dedicada accesible desde el perfil del estudiante que permite visualizar de forma organizada y cronolÃ³gica todas las actividades realizadas, con filtros por tema y detalles especÃ­ficos de resultados (puntajes, aciertos), facilitando la metacogniciÃ³n y el seguimiento de la evoluciÃ³n acadÃ©mica.


- **Registro de Usuarios (HU01):** Formulario para nuevos estudiantes con captura de datos acadÃ©micos (grado, secciÃ³n) y estilo visual gamificado.
- **Inicio de SesiÃ³n (HU02):** Sistema de autenticaciÃ³n seguro con soporte para sesiones persistentes y redirecciÃ³n dinÃ¡mica.
- **Cierre de SesiÃ³n (HU03):** FinalizaciÃ³n segura de sesiÃ³n con invalidaciÃ³n de credenciales y mensaje de retroalimentaciÃ³n.
- **VisualizaciÃ³n de Perfil (HU04):** Consulta de datos personales y acadÃ©micos con visualizaciÃ³n diferenciada por rol (Estudiante/Docente).
- **Banco de Problemas GeomÃ©tricos:** Ejercicios categorizados por tema y dificultad con soporte visual y teÃ³rico.
- **RetroalimentaciÃ³n Inmediata:** Explicaciones y correcciones en tiempo real tras cada respuesta del estudiante.
- **Sistema de GamificaciÃ³n:**
  - **Puntos (XP):** AcumulaciÃ³n de experiencia por actividades completadas.
  - **Insignias y Logros:** Reconocimientos automÃ¡ticos por constancia o metas alcanzadas.
  - **Niveles y Ranking:** VisualizaciÃ³n del progreso y posiciÃ³n relativa en el aprendizaje.
- **MÃ³dulos TemÃ¡ticos CrÃ­ticos:**
  - TriÃ¡ngulos y Ãngulos (Propiedades y resoluciÃ³n).
  - Segmentos y Rectas (Relaciones geomÃ©tricas bÃ¡sicas).
  - GeometrÃ­a Plana (Ãreas, perÃ­metros y razonamiento espacial).

## MetodologÃ­a y Enfoque PedagÃ³gico
- **ProgresiÃ³n por Dominio:** Asegurar que el estudiante comprenda un nivel antes de avanzar al siguiente.
- **EvaluaciÃ³n Formativa:** Uso del error como oportunidad de aprendizaje mediante feedback correctivo inmediato.
- **PrÃ¡ctica Guiada:** Apoyo con material teÃ³rico y videos recomendados segÃºn la necesidad del tema.
