from django.utils import timezone
from datetime import timedelta
from AppTutoria.models import ProgresoEstudiante
from AppGestionUsuario.services_gamification import GamificationService

def registrar_progreso(usuario, tema, tipo_actividad, referencia_id=None, porcentaje=0.0):
    """
    Registra el progreso de un estudiante en una actividad específica.
    Extrae automáticamente el grado y la sección del perfil del usuario.
    Asigna puntos de experiencia si es la primera vez que se realiza la actividad (HU22).
    
    Para Teoría: Crea registros históricos permitiendo múltiples sesiones por día (HU17/HU43).
    Si ya existe un registro en la última hora, lo actualiza (Sesión activa). 
    Si no, crea uno nuevo para el historial cronológico.
    """
    # 1. Verificar si ya existe CUALQUIER registro previo para puntos (HU22)
    query_params_puntos = {
        'usuario': usuario,
        'tema': tema,
        'tipo_actividad': tipo_actividad,
    }
    if tipo_actividad != 'Teoría':
        query_params_puntos['referencia_id'] = referencia_id

    ya_registrado_alguna_vez = ProgresoEstudiante.objects.filter(**query_params_puntos).exists()

    # 2. Lógica de Sesión para Teoría (HU43 - Historial Detallado)
    progreso = None
    if tipo_actividad == 'Teoría':
        # Buscamos si hay un registro de teoría para este tema en la última hora
        hace_una_hora = timezone.now() - timedelta(hours=1)
        progreso_reciente = ProgresoEstudiante.objects.filter(
            usuario=usuario,
            tema=tema,
            tipo_actividad='Teoría',
            fecha_registro__gte=hace_una_hora
        ).order_by('-fecha_registro').first()

        if progreso_reciente:
            # Actualizar la sesión actual
            progreso_reciente.referencia_id = referencia_id
            if porcentaje > float(progreso_reciente.porcentaje_completado):
                progreso_reciente.porcentaje_completado = porcentaje
            progreso_reciente.save()
            progreso = progreso_reciente
    
    # 3. Si no es teoría o es una nueva sesión de teoría, crear registro nuevo
    if not progreso:
        profile = getattr(usuario, 'profile', None)
        grado = (profile.grado if profile and profile.grado else 'N/A')[:10]
        seccion = (profile.seccion if profile and profile.seccion else 'N/A')[:10]
        
        progreso = ProgresoEstudiante.objects.create(
            usuario=usuario,
            tema=tema,
            tipo_actividad=tipo_actividad,
            grado=grado,
            seccion=seccion,
            referencia_id=referencia_id,
            porcentaje_completado=porcentaje
        )

    # 4. Asignar puntos si es la primera vez absoluto (Solo para Video y Teoría)
    if not ya_registrado_alguna_vez:
        if tipo_actividad == 'Video':
            GamificationService.assign_points_video(usuario)
        elif tipo_actividad == 'Teoría':
            GamificationService.assign_points_theory(usuario)

    return progreso
