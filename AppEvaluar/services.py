from typing import Dict, Optional
from django.contrib.auth.models import User
from .models import ResultadoDiagnostico, RespuestaUsuario

class SinResultadosError(Exception):
    """Excepción lanzada cuando un estudiante no tiene resultados de diagnóstico."""
    pass

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

    return mejor_recomendacion
