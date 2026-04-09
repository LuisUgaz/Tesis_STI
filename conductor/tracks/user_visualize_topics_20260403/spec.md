# Especificación: HU09 - Visualizar Temas Disponibles

## Resumen
Este track implementa la Historia de Usuario HU09: "Visualizar temas disponibles" para el Sistema Tutor Inteligente Adaptativo. El objetivo es presentar los temas de geometría a los estudiantes autenticados desde un modelo de base de datos, manteniendo el soporte para la lógica de recomendación previamente implementada (HU08).

## Requisitos Funcionales
- **Persistencia de Datos:** Crear el modelo `Tema` en la aplicación `AppTutoria` para almacenar los temas de geometría en la base de datos PostgreSQL.
- **Recuperación de Temas:** Obtener la lista de temas disponibles desde el modelo `Tema` en lugar de usar una lista hardcodeada.
- **Control de Acceso por Rol:** Asegurar que solo los usuarios autenticados con el rol de "Estudiante" puedan acceder al listado de temas.
- **Interfaz de Usuario:** Reutilizar y adaptar la plantilla `lista_temas.html` existente para mostrar el listado dinámico.
- **Integración de Recomendaciones:** Mantener el resaltado visual y el reordenamiento del tema "recomendado" si existe una `RecomendacionEstudiante` para el usuario actual (reutilizando la lógica de HU08).

## Requisitos No Funcionales
- **Consistencia:** Usar Django ORM y seguir las guías de estilo del proyecto.
- **Idioma:** Toda la documentación, consultas y acciones deben estar en español.
- **Seguridad:** Implementar una validación para restringir el acceso solo a estudiantes.

## Criterios de Aceptación
- Dado que el estudiante accede al menú de temas, el sistema debe mostrar los temas de geometría almacenados en la base de datos.
- El listado de temas debe ser accesible solo para estudiantes autenticados.
- El tema recomendado (si existe) debe aparecer priorizado y resaltado en la lista.

## Fuera de Alcance
- Carga del detalle de cada tema.
- Restricciones complejas de acceso más allá de la validación de rol.
- Nuevos algoritmos de recomendación.