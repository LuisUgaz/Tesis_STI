from AppTutoria.models import ProgresoEstudiante

def registrar_progreso(usuario, tema, tipo_actividad, referencia_id=None):
    """
    Registra el progreso de un estudiante en una actividad específica.
    Extrae automáticamente el grado y la sección del perfil del usuario.
    """
    profile = usuario.profile
    grado = profile.grado
    seccion = profile.seccion
    
    progreso = ProgresoEstudiante.objects.create(
        usuario=usuario,
        tema=tema,
        tipo_actividad=tipo_actividad,
        grado=grado,
        seccion=seccion,
        referencia_id=referencia_id
    )
    return progreso
