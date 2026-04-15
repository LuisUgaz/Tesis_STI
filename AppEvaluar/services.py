from typing import Dict, Optional
from django.contrib.auth.models import User
from .models import ResultadoDiagnostico, RespuestaUsuario, RecomendacionEstudiante, ResultadoEjercicio, Examen, Pregunta

class SinResultadosError(Exception):
    """Excepción lanzada cuando un estudiante no tiene resultados de diagnóstico."""
    pass

def asignar_preguntas_aleatorias(examen: Examen):
    """Busca preguntas disponibles para el tema del examen y las asigna aleatoriamente.
    
    Args:
        examen: El objeto Examen al cual se le asignarán las preguntas.
        
    Raises:
        ValueError: Si no existen suficientes preguntas disponibles para el tema.
    """
    # Filtrar preguntas: mismo tema, sin examen diagnóstico y sin examen de tema previo.
    preguntas_disponibles = Pregunta.objects.filter(
        tema=examen.tema,
        examen__isnull=True,
        examen_tema__isnull=True
    ).order_by('?') # Orden aleatorio
    
    if preguntas_disponibles.count() < examen.cantidad_preguntas:
        raise ValueError(
            f"No hay suficientes preguntas disponibles para el tema {examen.tema.nombre}. "
            f"Se requieren {examen.cantidad_preguntas} y solo hay {preguntas_disponibles.count()}."
        )
    
    # Tomar la cantidad necesaria y asignarlas
    seleccionadas = preguntas_disponibles[:examen.cantidad_preguntas]
    for pregunta in seleccionadas:
        pregunta.examen_tema = examen
        pregunta.save()

def calcular_recomendacion(estudiante: User) -> Optional[Dict]:
    """Calcula el tema que el estudiante debe reforzar basado en sus respuestas.

    Args:
        estudiante: El objeto User del estudiante para el cual se genera la
            recomendación.

    Returns:
        Un diccionario que contiene el tema recomendado y su métrica de
        desempeño (porcentaje de aciertos), o None si no se puede determinar.
        Ejemplo: {'tema': 'Ángulos', 'metrica': 25.0}

    Raises:
        SinResultadosError: Si el estudiante no tiene un ResultadoDiagnostico
            o no existen respuestas detalladas registradas.
    """
    if not ResultadoDiagnostico.objects.filter(estudiante=estudiante).exists():
        raise SinResultadosError(
            "El estudiante no tiene resultados de diagnóstico registrados.")
    
    respuestas = RespuestaUsuario.objects.filter(
        usuario=estudiante).select_related('pregunta', 'opcion_seleccionada')
    
    if not respuestas.exists():
        raise SinResultadosError(
            "No se encontraron respuestas detalladas para el estudiante.")

    resumen_temas: Dict[str, Dict] = {}

    for respuesta in respuestas:
        tema = respuesta.pregunta.categoria
        if tema not in resumen_temas:
            resumen_temas[tema] = {'correctas': 0, 'total': 0}
        
        resumen_temas[tema]['total'] += 1
        
        es_correcta = False
        if respuesta.pregunta.tipo == 'OPCION_MULTIPLE':
            if (respuesta.opcion_seleccionada and 
                respuesta.opcion_seleccionada.es_correcta):
                es_correcta = True
        
        if es_correcta:
            resumen_temas[tema]['correctas'] += 1

    mejor_recomendacion: Optional[Dict] = None
    min_porcentaje = 101.0

    # Ordenar temas alfabéticamente para asegurar consistencia en empates
    for tema in sorted(resumen_temas.keys()):
        datos = resumen_temas[tema]
        porcentaje = (datos['correctas'] / datos['total']) * 100
        
        if porcentaje < min_porcentaje:
            min_porcentaje = porcentaje
            mejor_recomendacion = {
                'tema': tema,
                'metrica': round(porcentaje, 2),
                'total_preguntas': datos['total'],
                'correctas': datos['correctas']
            }

    if mejor_recomendacion:
        # Persistir la recomendación (HU08)
        # Eliminamos previa para mantener solo una (la más reciente del diagnóstico)
        RecomendacionEstudiante.objects.filter(usuario=estudiante).delete()
        RecomendacionEstudiante.objects.create(
            usuario=estudiante,
            tema=mejor_recomendacion['tema'],
            metrica_desempeno=mejor_recomendacion['metrica']
        )

        # HU15: Ajuste de dificultad inicial basado en el diagnóstico
        # Regla: 0-40 (Básico), 41-75 (Intermedio), 76-100 (Avanzado)
        # Nota: Usamos la métrica del tema con menor desempeño para nivelar desde la base
        metrica = mejor_recomendacion['metrica']
        if metrica <= 40:
            nuevo_nivel = 'Básico'
        elif metrica <= 75:
            nuevo_nivel = 'Intermedio'
        else:
            nuevo_nivel = 'Avanzado'

        if hasattr(estudiante, 'profile'):
            estudiante.profile.nivel_dificultad_actual = nuevo_nivel
            estudiante.profile.save()

    return mejor_recomendacion

def ajustar_dificultad_estudiante(estudiante: User):
    """
    Analiza los últimos 5 resultados de ejercicios para ajustar el nivel del estudiante.
    Regla: >= 80% aciertos sube de nivel.
    """
    if not hasattr(estudiante, 'profile'):
        return

    # Obtener los últimos 5 resultados
    ultimos_resultados = ResultadoEjercicio.objects.filter(
        usuario=estudiante
    ).order_by('-fecha_resolucion')[:5]

    if ultimos_resultados.count() < 5:
        # No hay suficiente historia para ajustar
        return

    # Calcular desempeño en la sesión
    aciertos = sum(1 for r in ultimos_resultados if r.es_correcto)
    porcentaje = (aciertos / 5) * 100

    nivel_actual = estudiante.profile.nivel_dificultad_actual
    nuevo_nivel = nivel_actual

    if porcentaje >= 80:
        # Subir de nivel
        if nivel_actual == 'Básico':
            nuevo_nivel = 'Intermedio'
        elif nivel_actual == 'Intermedio':
            nuevo_nivel = 'Avanzado'
    
    # Por ahora no bajamos nivel para evitar desmotivación, solo mantenemos o subimos.
    
    if nuevo_nivel != nivel_actual:
        estudiante.profile.nivel_dificultad_actual = nuevo_nivel
        estudiante.profile.save()
