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
