from AppTutoria.models import ProgresoEstudiante
from AppGestionUsuario.services_gamification import GamificationService

def registrar_progreso(usuario, tema, tipo_actividad, referencia_id=None, porcentaje=0.0):
    """
    Registra el progreso de un estudiante en una actividad específica.
    Extrae automáticamente el grado y la sección del perfil del usuario.
    Asigna puntos de experiencia si es la primera vez que se realiza la actividad (HU22).
    Si es Teoría, actualiza el registro existente en lugar de crear uno nuevo.
    """
    # 1. Verificar si ya existe un registro previo para evitar duplicidad de puntos (HU22)
    query_params = {
        'usuario': usuario,
        'tema': tema,
        'tipo_actividad': tipo_actividad,
    }
    
    # Para Teoría, no filtramos por referencia_id porque queremos actualizar el único registro por tema
    if tipo_actividad != 'Teoría':
        query_params['referencia_id'] = referencia_id

    progreso_existente = ProgresoEstudiante.objects.filter(**query_params).first()
    ya_registrado = progreso_existente is not None

    profile = usuario.profile
    grado = profile.grado
    seccion = profile.seccion
    
    if tipo_actividad == 'Teoría' and ya_registrado:
        # Actualizar el registro existente
        progreso_existente.referencia_id = referencia_id
        # Solo actualizamos el porcentaje si es mayor al actual (evita retrocesos si el estudiante retrocede páginas)
        if porcentaje > float(progreso_existente.porcentaje_completado):
            progreso_existente.porcentaje_completado = porcentaje
        progreso_existente.save()
        progreso = progreso_existente
    else:
        # 2. Crear el registro de progreso (o primer registro de teoría)
        progreso = ProgresoEstudiante.objects.create(
            usuario=usuario,
            tema=tema,
            tipo_actividad=tipo_actividad,
            grado=grado,
            seccion=seccion,
            referencia_id=referencia_id,
            porcentaje_completado=porcentaje
        )

    # 3. Asignar puntos si es la primera vez (Solo para Video y Teoría, Ejercicios se manejan en su vista)
    if not ya_registrado:
        if tipo_actividad == 'Video':
            GamificationService.assign_points_video(usuario)
        elif tipo_actividad == 'Teoría':
            GamificationService.assign_points_theory(usuario)

    return progreso
