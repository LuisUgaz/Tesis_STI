import re
from AppEvaluar.models import (
    ResultadoDiagnostico, RecomendacionEstudiante, 
    ResultadoExamen, ControlPracticaTema
)
from .models import VideoTema, VisualizacionVideo, ProgresoEstudiante, Tema

def extraer_youtube_id(url):
    """
    Extrae el ID de un video de YouTube a partir de su URL.
    Soportar formatos: youtube.com/watch?v=ID, youtu.be/ID, youtube.com/embed/ID
    """
    if not url:
        return None
        
    regex = r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})'
    match = re.search(regex, url)
    if match:
        return match.group(1)
    return None

def generar_youtube_thumbnail(url):
    """
    Genera la URL de la miniatura de alta calidad para un video de YouTube.
    """
    video_id = extraer_youtube_id(url)
    if video_id:
        return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
    return None

def verificar_completitud_tema(usuario, tema):
    """
    Verifica si un estudiante ha completado todos los requisitos de un tema:
    1. Teoría al 100%
    2. Todos los videos vistos
    3. Práctica desbloqueada (Examen de tema habilitado)
    4. Al menos 4 exámenes aprobados (Nota >= 14 / Puntaje >= 70%)
    """
    # 1. Teoría al 100%
    teoria_completa = ProgresoEstudiante.objects.filter(
        usuario=usuario,
        tema=tema,
        tipo_actividad='Teoría',
        porcentaje_completado__gte=100.0
    ).exists()
    
    if not teoria_completa:
        return False, "Falta completar el material teórico al 100%."

    # 2. Videos vistos
    videos_activos = VideoTema.objects.filter(tema=tema, es_activo=True).count()
    if videos_activos > 0:
        videos_vistos = VisualizacionVideo.objects.filter(
            usuario=usuario,
            video__tema=tema,
            video__es_activo=True
        ).count()
        if videos_vistos < videos_activos:
            return False, f"Falta visualizar todos los videos del tema ({videos_vistos}/{videos_activos})."

    # 3. Práctica desbloqueada
    control_practica = ControlPracticaTema.objects.filter(usuario=usuario, tema=tema).first()
    if not control_practica or not control_practica.examen_desbloqueado:
        return False, "Falta completar la sesión de práctica (mínimo 80% de aciertos)."

    # 4. Al menos 4 exámenes aprobados (Puntaje >= 70% equivale a 14/20)
    examenes_aprobados = ResultadoExamen.objects.filter(
        estudiante=usuario,
        examen__tema=tema,
        puntaje__gte=70.0
    ).values('examen').distinct().count()
    
    if examenes_aprobados < 4:
        return False, f"Debes aprobar al menos 4 exámenes del tema (Llevas {examenes_aprobados}/4)."

    return True, "Tema completado."

def validar_estado_acceso_tema(usuario, tema_solicitado):
    """
    Valida si el usuario tiene permiso para acceder a un tema.
    Retorna (es_permitido, codigo_error, tema_pendiente_nombre)
    """
    # Los docentes y administradores tienen acceso total
    if not hasattr(usuario, 'profile') or usuario.profile.rol != 'Estudiante':
        return True, None, None

    # 1. Verificar Diagnóstico
    if not ResultadoDiagnostico.objects.filter(estudiante=usuario).exists():
        return False, 'FALTA_DIAGNOSTICO', None

    # 2. Verificar Recomendación
    recomendacion = RecomendacionEstudiante.objects.filter(usuario=usuario).first()
    if not recomendacion:
        return True, None, None

    # Si el tema solicitado es el recomendado, acceso permitido siempre
    if tema_solicitado.nombre == recomendacion.tema:
        return True, None, None

    # Si solicita otro tema, debemos verificar si el recomendado ya fue completado
    tema_recomendado_obj = Tema.objects.filter(nombre=recomendacion.tema).first()
    if not tema_recomendado_obj:
        return True, None, None

    completado, mensaje = verificar_completitud_tema(usuario, tema_recomendado_obj)
    if not completado:
        return False, 'TEMA_PENDIENTE', tema_recomendado_obj.nombre

    return True, None, None

def obtener_siguiente_tema_diagnostico(usuario):
    """
    Calcula los temas evaluados en el examen diagnóstico del estudiante y devuelve
    el siguiente tema con menor desempeño (PDP más bajo) que aún no ha sido completado.
    """
    from AppEvaluar.models import RespuestaUsuario
    from django.db.models import Avg, StdDev
    
    try:
        # 1. Verificar Diagnóstico
        if not ResultadoDiagnostico.objects.filter(estudiante=usuario).exists():
            return None

        respuestas = RespuestaUsuario.objects.filter(
            usuario=usuario
        ).select_related('pregunta', 'opcion_seleccionada', 'pregunta__tema')

        if not respuestas.exists():
            return None

        resumen_temas = {}
        pesos_dificultad = {'Básico': 3, 'Intermedio': 2, 'Avanzado': 1}

        # Estadísticas globales para normalización de tiempo
        stats_tiempo = RespuestaUsuario.objects.filter(
            opcion_seleccionada__es_correcta=True
        ).values('pregunta_id').annotate(
            promedio=Avg('tiempo_respuesta'),
            desviacion=StdDev('tiempo_respuesta')
        )
        dict_stats = {s['pregunta_id']: s for s in stats_tiempo}

        for respuesta in respuestas:
            pregunta = respuesta.pregunta
            if not pregunta.tema:
                continue
            tema_nombre = pregunta.tema.nombre
            dificultad = pregunta.dificultad or 'Básico'
            peso = pesos_dificultad.get(dificultad, 1)

            if tema_nombre not in resumen_temas:
                resumen_temas[tema_nombre] = {'score_obtenido': 0.0, 'score_maximo': 0}
            
            resumen_temas[tema_nombre]['score_maximo'] += peso
            
            es_correcta = False
            if respuesta.opcion_seleccionada and respuesta.opcion_seleccionada.es_correcta:
                es_correcta = True
            
            if es_correcta:
                puntos_ganados = float(peso)
                if respuesta.tiempo_respuesta:
                    stats = dict_stats.get(pregunta.id)
                    if stats and stats['promedio'] and stats['desviacion']:
                        promedio = float(stats['promedio'])
                        desviacion = float(stats['desviacion'])
                        if desviacion > 0:
                            z_score = (respuesta.tiempo_respuesta - promedio) / desviacion
                            if z_score > 1.5:
                                puntos_ganados *= (1 - min(0.3, (z_score - 1.5) * 0.1))
                
                resumen_temas[tema_nombre]['score_obtenido'] += puntos_ganados

        # Calcular PDP por tema
        lista_desempeno = []
        for tema_nombre, datos in resumen_temas.items():
            pdp = (datos['score_obtenido'] / datos['score_maximo']) * 100 if datos['score_maximo'] > 0 else 0
            lista_desempeno.append({
                'tema_nombre': tema_nombre,
                'pdp': pdp
            })

        # Ordenar por PDP de menor a mayor (peores temas primero)
        lista_desempeno.sort(key=lambda x: x['pdp'])

        # Buscar el primer tema que no esté completado por el estudiante
        for item in lista_desempeno:
            tema_obj = Tema.objects.filter(nombre=item['tema_nombre']).first()
            if tema_obj:
                completado, _ = verificar_completitud_tema(usuario, tema_obj)
                if not completado:
                    return tema_obj
    except Exception:
        # Retorno seguro en caso de cualquier error
        return None

    return None

