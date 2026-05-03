import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from AppEvaluar.models import RecomendacionEstudiante, ExamenDiagnostico, Examen
from AppEvaluar.views import student_required
from .models import Tema, ContenidoTema, VideoTema, VisualizacionVideo, ProgresoEstudiante
from .services import registrar_progreso

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import VideoTemaForm

class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and hasattr(self.request.user, 'profile') and self.request.user.profile.rol == 'Docente'

class VideoTemaListView(LoginRequiredMixin, TeacherRequiredMixin, ListView):
    model = VideoTema
    template_name = 'AppTutoria/video_gestion_list.html'
    context_object_name = 'videos'
    ordering = ['tema', 'orden']

    def get_queryset(self):
        """
        Retorna solo los videos activos para la gestión del docente.
        """
        return VideoTema.objects.filter(es_activo=True).order_by('tema', 'orden')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['temas'] = Tema.objects.all()
        return context

class VideoTemaCreateView(LoginRequiredMixin, TeacherRequiredMixin, CreateView):
    model = VideoTema
    form_class = VideoTemaForm
    template_name = 'AppTutoria/video_registro_form.html'
    success_url = reverse_lazy('tutoria:video_gestion_list')

    def form_valid(self, form):
        messages.success(self.request, "Video recomendado registrado exitosamente.")
        return super().form_valid(form)

class VideoTemaDeleteView(LoginRequiredMixin, TeacherRequiredMixin, DeleteView):
    model = VideoTema
    success_url = reverse_lazy('tutoria:video_gestion_list')

    def post(self, request, *args, **kwargs):
        """
        Sobrescribe el método post para realizar un borrado lógico.
        """
        video = self.get_object()
        video.es_activo = False
        video.save()
        messages.success(request, f"El video '{video.titulo}' ha sido eliminado exitosamente.")
        return redirect(self.success_url)

    def delete(self, request, *args, **kwargs):
        """
        Sobrescribe delete para redirigir a post (Django DeleteView usa delete internamente).
        """
        return self.post(request, *args, **kwargs)

@login_required
def lista_temas(request):
    """
    Muestra la lista de temas geométricos obtenidos de la BD, resaltando el recomendado para estudiantes.
    Los docentes pueden ver todos los temas sin restricciones.
    """
    # Verificar que el usuario tenga el perfil adecuado
    if not hasattr(request.user, 'profile') or request.user.profile.rol not in ['Estudiante', 'Docente']:
        raise PermissionDenied("No tienes permiso para acceder a la lista de temas.")

    # Lista de temas desde la base de datos con sus exámenes asociados
    temas_qs = Tema.objects.prefetch_related('examenes').all()
    temas_db = list(temas_qs)
    
    # Obtener recomendación (HU08) - Solo aplica lógica visual para estudiantes
    recomendacion = None
    examen = None
    if request.user.profile.rol == 'Estudiante':
        examen = ExamenDiagnostico.objects.first()
        recomendacion = RecomendacionEstudiante.objects.filter(usuario=request.user).first()
        if recomendacion:
            tema_recomendado_obj = next((t for t in temas_db if t.nombre == recomendacion.tema), None)
            if tema_recomendado_obj:
                temas_db.remove(tema_recomendado_obj)
                temas_db.insert(0, tema_recomendado_obj)

    return render(request, 'AppTutoria/lista_temas.html', {
        'temas': temas_db,
        'recomendacion': recomendacion,
        'examen': examen
    })

@login_required
def tema_detalle(request, slug):
    """
    Muestra el contenido detallado de un tema específico.
    Los docentes supervisan todo. Los estudiantes siguen su ruta recomendada.
    """
    if not hasattr(request.user, 'profile') or request.user.profile.rol not in ['Estudiante', 'Docente']:
        raise PermissionDenied("Acceso no autorizado.")

    # 2. Obtener el tema por slug
    tema = get_object_or_404(Tema, slug=slug)
    es_docente = request.user.profile.rol == 'Docente'

    # 3. Verificar recomendación solo para estudiantes
    if not es_docente:
        esta_recomendado = RecomendacionEstudiante.objects.filter(
            usuario=request.user, 
            tema=tema.nombre
        ).exists()

        if not esta_recomendado:
            messages.info(request, "Para acceder a este tema, primero debes realizar tu examen diagnóstico inicial.", extra_tags='needs_exam')
            return redirect('tutoria:lista_temas')

    # 4. Obtener la sección solicitada (por defecto 'resumen')
    seccion = request.GET.get('seccion', 'resumen')

    # 5. Obtener el contenido asociado
    contenido = None
    if seccion == 'teoria':
        contenido = get_object_or_404(ContenidoTema, tema=tema)
        # Registrar progreso SOLO para estudiantes
        if not es_docente:
            registrar_progreso(
                usuario=request.user,
                tema=tema,
                tipo_actividad='Teoría'
            )
    
    # HU41: Obtener exámenes asociados al tema ordenados cronológicamente
    examenes_qs = Examen.objects.filter(tema=tema).order_by('fecha_creacion')
    examenes = []
    
    if not es_docente:
        # Lógica de bloqueo secuencial para estudiantes
        proximo_bloqueado = False
        from AppEvaluar.models import ResultadoExamen
        
        for i, ex en enumerate(examenes_qs):
            # Verificar si ya resolvió este examen
            ha_resuelto = ResultadoExamen.objects.filter(estudiante=request.user, examen=ex).exists()
            
            # El examen está disponible si:
            # 1. Es el primero (index 0)
            # 2. El anterior ya fue resuelto
            esta_bloqueado = proximo_bloqueado
            
            # Si el actual no ha sido resuelto, el siguiente debe bloquearse
            if not ha_resuelto:
                proximo_bloqueado = True
            
            # Añadir metadatos al objeto para el template
            ex.esta_bloqueado = esta_bloqueado
            ex.ha_resuelto = ha_resuelto
            ex.indice = i + 1 # Para mostrar Examen 1, Examen 2...
            examenes.append(ex)
    else:
        # Los docentes ven todo desbloqueado
        for i, ex en enumerate(examenes_qs):
            ex.esta_bloqueado = False
            ex.indice = i + 1
            examenes.append(ex)
    
    return render(request, 'AppTutoria/tema_detalle.html', {
        'tema': tema,
        'contenido': contenido,
        'seccion': seccion,
        'es_docente': es_docente,
        'examenes': examenes
    })

@login_required
def video_list(request, slug):
    """
    Muestra la lista de videos asociados a un tema específico.
    """
    if not hasattr(request.user, 'profile') or request.user.profile.rol not in ['Estudiante', 'Docente']:
        raise PermissionDenied("Acceso denegado.")

    # 2. Obtener el tema por slug
    tema = get_object_or_404(Tema, slug=slug)
    es_docente = request.user.profile.rol == 'Docente'

    # 3. Validar recomendación solo para estudiantes
    if not es_docente:
        esta_recomendado = RecomendacionEstudiante.objects.filter(
            usuario=request.user, 
            tema=tema.nombre
        ).exists()

        if not esta_recomendado:
            messages.info(request, "Para acceder a los videos, primero debes realizar tu examen diagnóstico inicial.", extra_tags='needs_exam')
            return redirect('tutoria:lista_temas')

    # 4. Obtener los videos asociados al tema (solo activos)
    videos = VideoTema.objects.filter(tema=tema, es_activo=True)

    return render(request, 'AppTutoria/videos.html', {
        'tema': tema,
        'videos': videos,
        'es_docente': es_docente
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
        return JsonResponse({'error': 'Acceso denegado. Debes realizar el examen diagnóstico.'}, status=403)

    # Registrar o actualizar contador
    visualizacion, created = VisualizacionVideo.objects.get_or_create(
        usuario=request.user,
        video=video,
        defaults={'contador': 1}
    )

    if not created:
        visualizacion.contador += 1
        visualizacion.save()

    # Registrar progreso centralizado (HU17)
    registrar_progreso(
        usuario=request.user,
        tema=video.tema,
        tipo_actividad='Video',
        referencia_id=video.id
    )

    return JsonResponse({
        'status': 'success',
        'contador': visualizacion.contador,
        'video': video.titulo
    })

@login_required
@student_required
@require_POST
def actualizar_progreso_teoria(request):
    """
    Actualiza el progreso de teoría mediante AJAX (HU43).
    Recibe tema_id, pagina_actual y total_paginas.
    """
    try:
        data = json.loads(request.body)
        tema_id = data.get('tema_id')
        pagina_actual = data.get('pagina_actual')
        total_paginas = data.get('total_paginas')

        if not all([tema_id, pagina_actual, total_paginas]):
            return JsonResponse({'success': False, 'error': 'Faltan parámetros'}, status=400)

        tema = get_object_or_404(Tema, id=tema_id)
        
        # Calcular porcentaje
        porcentaje = (pagina_actual / total_paginas) * 100
        
        # Registrar o actualizar progreso
        registrar_progreso(
            usuario=request.user,
            tema=tema,
            tipo_actividad='Teoría',
            referencia_id=pagina_actual,
            porcentaje=porcentaje
        )

        return JsonResponse({'success': True, 'porcentaje': porcentaje})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
