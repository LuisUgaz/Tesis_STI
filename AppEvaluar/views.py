from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponseBadRequest
from .models import (
    ExamenDiagnostico, Pregunta, Opcion, RespuestaUsuario, 
    ResultadoDiagnostico, RecomendacionEstudiante,
    Ejercicio, OpcionEjercicio, ResultadoEjercicio
)
from .services import calcular_recomendacion, ajustar_dificultad_estudiante
from .services_metrics import actualizar_metricas_estudiante
from AppTutoria.services import registrar_progreso
from AppGestionUsuario.services_gamification import GamificationService
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from AppTutoria.models import Tema

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from AppTutoria.models import Tema, ProgresoEstudiante

def student_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.profile.rol != 'Estudiante':
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func

class StudentRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.profile.rol == 'Estudiante'

class HistorialResultadosView(LoginRequiredMixin, StudentRequiredMixin, ListView):
    model = ProgresoEstudiante
    template_name = 'AppEvaluar/historial_resultados.html'
    context_object_name = 'progresos'

    def get_queryset(self):
        queryset = ProgresoEstudiante.objects.filter(usuario=self.request.user)
        
        # Filtro por tema
        tema_id = self.request.GET.get('tema')
        if tema_id:
            queryset = queryset.filter(tema_id=tema_id)
        
        # Filtro por fecha inicio
        fecha_inicio = self.request.GET.get('fecha_inicio')
        if fecha_inicio:
            queryset = queryset.filter(fecha_registro__date__gte=fecha_inicio)
            
        # Filtro por fecha fin
        fecha_fin = self.request.GET.get('fecha_fin')
        if fecha_fin:
            queryset = queryset.filter(fecha_registro__date__lte=fecha_fin)
        
        # Ordenamiento
        order = self.request.GET.get('order', 'desc')
        if order == 'asc':
            queryset = queryset.order_by('fecha_registro')
        else:
            queryset = queryset.order_by('-fecha_registro')
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['temas'] = Tema.objects.all()
        context['tema_seleccionado'] = self.request.GET.get('tema', '')
        context['fecha_inicio'] = self.request.GET.get('fecha_inicio', '')
        context['fecha_fin'] = self.request.GET.get('fecha_fin', '')
        context['orden_actual'] = self.request.GET.get('order', 'desc')
        return context

@login_required
@student_required
def iniciar_practica(request):
    """
    Selecciona ejercicios del tema recomendado y nivel del estudiante.
    Muestra la interfaz de resolución secuencial.
    """
    # 1. Obtener la recomendación actual
    recomendacion = RecomendacionEstudiante.objects.filter(usuario=request.user).first()
    
    if not recomendacion:
        raise PermissionDenied("Debes rendir tu examen diagnóstico para recibir recomendaciones de práctica.")

    # 2. Obtener el tema asociado
    tema = get_object_or_404(Tema, nombre=recomendacion.tema)

    # 3. Filtrar ejercicios por Tema y Nivel del Perfil (HU15)
    nivel = request.user.profile.nivel_dificultad_actual
    ejercicios = Ejercicio.objects.filter(
        tema=tema, 
        dificultad=nivel
    ).prefetch_related('opciones').order_by('?')[:5]

    if not ejercicios.exists():
        messages.info(request, f"Aún no hay ejercicios de nivel {nivel} para el tema: {tema.nombre}")
        # Fallback: Si no hay del nivel, mostrar cualquiera del tema para no bloquear al alumno
        ejercicios = Ejercicio.objects.filter(tema=tema).prefetch_related('opciones').order_by('?')[:5]
        
    if not ejercicios.exists():
        messages.info(request, f"Aún no hay ejercicios cargados para el tema: {tema.nombre}")
        return redirect('lista_temas')

    return render(request, 'AppEvaluar/practica_ejercicio.html', {
        'tema': tema,
        'ejercicios': ejercicios,
        'total': ejercicios.count()
    })

@login_required
@student_required
def validar_respuesta(request):
    """
    Endpoint AJAX para validar la opción seleccionada y guardar el resultado.
    """
    if request.method != 'POST':
        return HttpResponseBadRequest("Método no permitido")

    ejercicio_id = request.POST.get('ejercicio_id')
    opcion_id = request.POST.get('opcion_id')
    tiempo = request.POST.get('tiempo', 0)

    ejercicio = get_object_or_404(Ejercicio, id=ejercicio_id)
    opcion = get_object_or_404(OpcionEjercicio, id=opcion_id, ejercicio=ejercicio)

    # Feedback combinado para persistencia (HU16)
    feedback_especifico = opcion.retroalimentacion or ("¡Correcto!" if opcion.es_correcta else "Sigue intentándolo.")
    explicacion_tecnica = ejercicio.explicacion_tecnica or ""
    feedback_completo = f"{feedback_especifico} {explicacion_tecnica}".strip()

    # Persistir el resultado
    resultado_ej = ResultadoEjercicio.objects.create(
        usuario=request.user,
        ejercicio=ejercicio,
        es_correcto=opcion.es_correcta,
        tiempo_empleado=int(tiempo),
        feedback_mostrado=feedback_completo
    )

    # Actualizar mÃ©tricas acadÃ©micas (HU20)
    actualizar_metricas_estudiante(request.user, actividad_reciente=resultado_ej)

    # Registrar progreso centralizado (HU17)
    registrar_progreso(
        usuario=request.user,
        tema=ejercicio.tema,
        tipo_actividad='Ejercicio',
        referencia_id=ejercicio.id
    )

    # HU15: Intentar ajustar dificultad tras la respuesta
    ajustar_dificultad_estudiante(request.user)

    # Asignar puntos por actividad (HU22)
    puntos_ganados = GamificationService.assign_points_exercise(
        request.user, 
        is_correct=opcion.es_correcta, 
        difficulty=ejercicio.dificultad
    )

    # Refrescar perfil para obtener puntos actualizados
    request.user.profile.refresh_from_db()

    return JsonResponse({
        'es_correcto': opcion.es_correcta,
        'feedback': feedback_especifico,
        'explicacion_tecnica': explicacion_tecnica,
        'puntos_ganados': puntos_ganados,
        'total_puntos': request.user.profile.puntos_acumulados
    })

@login_required
@student_required
def rendir_examen(request, examen_id):
    examen = get_object_or_404(ExamenDiagnostico, id=examen_id)
    
    # Validar si el estudiante ya realizó el examen (HU06)
    if ResultadoDiagnostico.objects.filter(estudiante=request.user, examen=examen).exists():
        messages.error(request, "Ya has realizado este examen diagnóstico.")
        return redirect('ver_resultados', examen_id=examen.id)

    preguntas = examen.preguntas.all().prefetch_related('opciones')
    
    if request.method == 'GET':
        # Guardar hora de inicio en la sesión si no existe para este examen
        session_key = f'inicio_examen_{examen_id}'
        if session_key not in request.session:
            request.session[session_key] = timezone.now().isoformat()
    
    if request.method == 'POST':
        # Validar tiempo en el backend
        session_key = f'inicio_examen_{examen_id}'
        inicio_str = request.session.get(session_key)
        
        if inicio_str:
            inicio = timezone.datetime.fromisoformat(inicio_str)
            # Damos 1 minuto extra de tolerancia por latencia de red
            tiempo_maximo = inicio + timedelta(minutes=examen.tiempo_limite + 1)
            
            if timezone.now() > tiempo_maximo:
                messages.error(request, "El tiempo del examen ha expirado.")
                # Aún así guardamos lo que llegó, o podríamos rechazarlo. 
                # Por requerimiento, solemos guardar lo enviado.
        
        # Eliminar respuestas previas (si las hubiera, aunque el bloqueo anterior lo previene)
        RespuestaUsuario.objects.filter(usuario=request.user, pregunta__examen=examen).delete()
        
        total_correctas = 0
        total_preguntas = preguntas.count()

        for pregunta in preguntas:
            campo_nombre = f'pregunta_{pregunta.id}'
            valor = request.POST.get(campo_nombre)
            
            if valor:
                respuesta = RespuestaUsuario(
                    usuario=request.user,
                    pregunta=pregunta
                )
                
                if pregunta.tipo == 'OPCION_MULTIPLE':
                    try:
                        opcion = Opcion.objects.get(id=valor, pregunta=pregunta)
                        respuesta.opcion_seleccionada = opcion
                        if opcion.es_correcta:
                            total_correctas += 1
                    except (Opcion.DoesNotExist, ValueError):
                        continue
                else:
                    respuesta.respuesta_texto = valor
                
                respuesta.save()
        
        # Calcular puntaje (HU06: Respuestas Correctas / Total de Preguntas * 100)
        puntaje = (total_correctas / total_preguntas * 100) if total_preguntas > 0 else 0
        
        # Persistir resultado (HU06)
        resultado_diag = ResultadoDiagnostico.objects.create(
            estudiante=request.user,
            examen=examen,
            puntaje=puntaje
        )

        # Actualizar mÃ©tricas acadÃ©micas (HU20)
        actualizar_metricas_estudiante(request.user, actividad_reciente=resultado_diag)

        # Registrar progreso centralizado por tema (HU17)
        temas_evaluados = preguntas.values_list('categoria', flat=True).distinct()
        for nombre_tema in temas_evaluados:
            tema_obj = Tema.objects.filter(nombre=nombre_tema).first()
            if tema_obj:
                registrar_progreso(
                    usuario=request.user,
                    tema=tema_obj,
                    tipo_actividad='Examen',
                    referencia_id=examen.id
                )

        # Generar y persistir recomendación (HU08)
        try:
            calcular_recomendacion(request.user)
        except Exception:
            # Si algo falla en la recomendación, no bloqueamos el flujo principal
            pass

        # Limpiar sesión
        if session_key in request.session:
            del request.session[session_key]
            
        messages.success(request, "¡Examen enviado con éxito!")
        return redirect('ver_resultados', examen_id=examen.id)
        
    return render(request, 'AppEvaluar/rendir_examen.html', {
        'examen': examen,
        'preguntas': preguntas
    })

@login_required
@student_required
def ver_resultados(request, examen_id):
    examen = get_object_or_404(ExamenDiagnostico, id=examen_id)
    respuestas = RespuestaUsuario.objects.filter(usuario=request.user, pregunta__examen=examen)
    resultado_persistido = ResultadoDiagnostico.objects.filter(estudiante=request.user, examen=examen).first()
    
    if not respuestas.exists() and not resultado_persistido:
        messages.warning(request, "No tienes resultados para este examen.")
        return redirect('home')

    total_preguntas = examen.preguntas.count()
    total_correctas = 0
    resumen_temas = {}

    # Si hay respuestas, calculamos el resumen por temas (esto es para el detalle visual)
    if respuestas.exists():
        for respuesta in respuestas:
            tema = respuesta.pregunta.categoria
            if tema not in resumen_temas:
                resumen_temas[tema] = {'correctas': 0, 'total': 0}
            
            resumen_temas[tema]['total'] += 1
            
            es_correcta = False
            if respuesta.pregunta.tipo == 'OPCION_MULTIPLE':
                if respuesta.opcion_seleccionada and respuesta.opcion_seleccionada.es_correcta:
                    es_correcta = True
            
            if es_correcta:
                total_correctas += 1
                resumen_temas[tema]['correctas'] += 1

        # Calcular porcentajes por tema
        for tema, datos in resumen_temas.items():
            datos['porcentaje'] = round((datos['correctas'] / datos['total']) * 100, 2)

    # El puntaje total lo tomamos del persistido si existe, si no, lo calculamos (compatibilidad)
    if resultado_persistido:
        # El modelo guarda sobre 100, pero la vista actual muestra sobre 20
        puntaje_total = round(float(resultado_persistido.puntaje) * 20 / 100, 2)
    else:
        puntaje_total = round((total_correctas / total_preguntas) * 20, 2) if total_preguntas > 0 else 0

    return render(request, 'AppEvaluar/resultados.html', {
        'examen': examen,
        'puntaje_total': puntaje_total,
        'total_correctas': total_correctas,
        'total_preguntas': total_preguntas,
        'resumen_temas': resumen_temas
    })
