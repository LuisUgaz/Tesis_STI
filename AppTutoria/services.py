from AppTutoria.models import ProgresoEstudiante
from AppGestionUsuario.services_gamification import GamificationService

def registrar_progreso(usuario, tema, tipo_actividad, referencia_id=None):
    """
    Registra el progreso de un estudiante en una actividad específica.
    Extrae automáticamente el grado y la sección del perfil del usuario.
    Asigna puntos de experiencia si es la primera vez que se realiza la actividad (HU22).
    """
    # 1. Verificar si ya existe un registro previo para evitar duplicidad de puntos (HU22)
    ya_registrado = ProgresoEstudiante.objects.filter(
        usuario=usuario,
        tema=tema,
        tipo_actividad=tipo_actividad,
        referencia_id=referencia_id
    ).exists()

    profile = usuario.profile
    grado = profile.grado
    seccion = profile.seccion
    
    # 2. Crear el registro de progreso
    progreso = ProgresoEstudiante.objects.create(
        usuario=usuario,
        tema=tema,
        tipo_actividad=tipo_actividad,
        grado=grado,
        seccion=seccion,
        referencia_id=referencia_id
    )

    # 3. Asignar puntos si es la primera vez (Solo para Video y Teoría, Ejercicios se manejan en su vista)
    if not ya_registrado:
        if tipo_actividad == 'Video':
            GamificationService.assign_points_video(usuario)
        elif tipo_actividad == 'Teoría':
            GamificationService.assign_points_theory(usuario)

    return progreso
