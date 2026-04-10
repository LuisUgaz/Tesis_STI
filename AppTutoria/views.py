from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from AppEvaluar.models import RecomendacionEstudiante
from .models import Tema, ContenidoTema, VideoTema, VisualizacionVideo

@login_required
def lista_temas(request):
    """
    Muestra la lista de temas geométricos obtenidos de la BD, resaltando el recomendado.
    """
    # Verificar que el usuario tenga el perfil de Estudiante
    if not hasattr(request.user, 'profile') or request.user.profile.rol != 'Estudiante':
        raise PermissionDenied("Solo los estudiantes pueden acceder a la lista de temas.")

    # Lista de temas desde la base de datos
    temas_db = list(Tema.objects.all())
    
    # Obtener recomendación (HU08)
    recomendacion = RecomendacionEstudiante.objects.filter(usuario=request.user).first()
    
    # Lógica de reordenamiento basada en la recomendación
    if recomendacion:
        # Buscar el tema en la lista de temas_db que coincida con el nombre de la recomendación
        tema_recomendado_obj = next((t for t in temas_db if t.nombre == recomendacion.tema), None)
        
        if tema_recomendado_obj:
            # Reordenar: colocar el objeto tema recomendado al principio
            temas_db.remove(tema_recomendado_obj)
            temas_db.insert(0, tema_recomendado_obj)

    return render(request, 'AppTutoria/lista_temas.html', {
        'temas': temas_db,
        'recomendacion': recomendacion
    })

@login_required
def tema_detalle(request, slug):
    """
    Muestra el contenido detallado de un tema específico si el usuario tiene permiso.
    Permite navegar entre secciones (resumen, teoria, ejercicios, videos).
    """
    # 1. Verificar rol de Estudiante
    if not hasattr(request.user, 'profile') or request.user.profile.rol != 'Estudiante':
        raise PermissionDenied("Solo los estudiantes pueden acceder al contenido de estudio.")

    # 2. Obtener el tema por slug
    tema = get_object_or_404(Tema, slug=slug)

    # 3. Verificar si el tema está recomendado para el estudiante
    esta_recomendado = RecomendacionEstudiante.objects.filter(
        usuario=request.user, 
        tema=tema.nombre
    ).exists()

    if not esta_recomendado:
        raise PermissionDenied("No tienes acceso a este tema aún. Debes seguir tu ruta recomendada.")

    # 4. Obtener la sección solicitada (por defecto 'resumen')
    seccion = request.GET.get('seccion', 'resumen')

    # 5. Obtener el contenido asociado si es necesario
    contenido = None
    if seccion == 'teoria':
        contenido = get_object_or_404(ContenidoTema, tema=tema)
    
    return render(request, 'AppTutoria/tema_detalle.html', {
        'tema': tema,
        'contenido': contenido,
        'seccion': seccion
    })

@login_required
def video_list(request, slug):
    """
    Muestra la lista de videos asociados a un tema específico.
    Valida que el estudiante tenga acceso al tema según sus recomendaciones.
    """
    # 1. Verificar rol de Estudiante
    if not hasattr(request.user, 'profile') or request.user.profile.rol != 'Estudiante':
        raise PermissionDenied("Solo los estudiantes pueden acceder a los videos.")

    # 2. Obtener el tema por slug
    tema = get_object_or_404(Tema, slug=slug)

    # 3. Verificar si el tema está recomendado para el estudiante
    esta_recomendado = RecomendacionEstudiante.objects.filter(
        usuario=request.user, 
        tema=tema.nombre
    ).exists()

    if not esta_recomendado:
        raise PermissionDenied("No tienes acceso a los videos de este tema aún.")

    # 4. Obtener los videos asociados al tema
    videos = VideoTema.objects.filter(tema=tema)

    return render(request, 'AppTutoria/videos.html', {
        'tema': tema,
        'videos': videos
    })

@login_required
@require_POST
def registrar_visualizacion(request):
    """
    Endpoint AJAX para registrar que un estudiante terminó de ver un video.
    """
    video_id = request.POST.get('video_id')
    if not video_id:
        return JsonResponse({'error': 'ID de video no proporcionado'}, status=400)

    video = get_object_or_404(VideoTema, id=video_id)

    # Validar permiso (mismo que en video_list)
    esta_recomendado = RecomendacionEstudiante.objects.filter(
        usuario=request.user, 
        tema=video.tema.nombre
    ).exists()

    if not esta_recomendado:
        raise PermissionDenied("No tienes permiso para registrar visualizaciones de este tema.")

    # Registrar o actualizar contador
    visualizacion, created = VisualizacionVideo.objects.get_or_create(
        usuario=request.user,
        video=video,
        defaults={'contador': 1}
    )

    if not created:
        visualizacion.contador += 1
        visualizacion.save()

    return JsonResponse({
        'status': 'success',
        'contador': visualizacion.contador,
        'video': video.titulo
    })
