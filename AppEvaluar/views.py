from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponseBadRequest
from .models import (
    ExamenDiagnostico, Examen, Pregunta, Opcion, RespuestaUsuario, 
    ResultadoDiagnostico, RecomendacionEstudiante,
    Ejercicio, OpcionEjercicio, ResultadoEjercicio
)
from .services import calcular_recomendacion, ajustar_dificultad_estudiante, asignar_preguntas_aleatorias, obtener_feedback_ia, evaluar_exito_recomendacion
from .services_metrics import actualizar_metricas_estudiante, get_classroom_performance_summary
from AppTutoria.services import registrar_progreso
from AppGestionUsuario.models import Profile, MetricasEstudiante
from django.db.models import Count, Q
import json
from AppGestionUsuario.services_gamification import GamificationService
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from AppTutoria.models import Tema

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from AppTutoria.models import Tema, ProgresoEstudiante
from .services_export import generar_excel_reporte_docente
from django.http import HttpResponse
from .forms import EjercicioForm, OpcionEjercicioFormSet, ExamenForm
from django.db import transaction
from .utils_import import extraer_texto_pdf, extraer_texto_docx, analizar_preguntas_con_gemini
from django.views import View

def student_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.profile.rol != 'Estudiante':
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func

class StudentRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.profile.rol == 'Estudiante'

class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        # Permitir tanto si tiene el rol de Docente en el perfil como si es is_staff (admin)
        return self.request.user.is_authenticated and (
            (hasattr(self.request.user, 'profile') and self.request.user.profile.rol == 'Docente') or 
            self.request.user.is_staff
        )

class IAFeedbackView(LoginRequiredMixin, View):
    """
    Endpoint AJAX para obtener la retroalimentación de la IA para una pregunta específica (HU40).
    """
    def get(self, request, respuesta_id):
        respuesta = get_object_or_404(RespuestaUsuario, id=respuesta_id)
        
        # Seguridad: Solo el dueño de la respuesta puede pedir el feedback
        if respuesta.usuario != request.user:
            return JsonResponse({'error': 'No autorizado'}, status=403)
        
        feedback = obtener_feedback_ia(respuesta)
        return JsonResponse({'feedback': feedback})

class ExamenDashboardView(LoginRequiredMixin, TeacherRequiredMixin, ListView):
    model = Examen
    template_name = 'AppEvaluar/examen_dashboard.html'
    context_object_name = 'examenes'
    ordering = ['-fecha_creacion']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Resumen de preguntas disponibles por tema
        # Preguntas que NO tienen examen diagnóstico ni examen de tema
        temas_con_conteo = Tema.objects.annotate(
            preguntas_disponibles=Count(
                'preguntas_diagnostico',
                filter=Q(preguntas_diagnostico__examen__isnull=True, 
                         preguntas_diagnostico__examen_tema__isnull=True)
            )
        )
        context['temas_indicadores'] = temas_con_conteo
        return context

class ExamenCreateView(LoginRequiredMixin, TeacherRequiredMixin, CreateView):
    model = Examen
    form_class = ExamenForm
    template_name = 'AppEvaluar/examen_form.html'
    success_url = reverse_lazy('evaluar:examen_dashboard')

    def form_valid(self, form):
        try:
            with transaction.atomic():
                # Primero guardamos el examen (sin preguntas aún)
                self.object = form.save()
                # Luego asignamos las preguntas aleatorias
                asignar_preguntas_aleatorias(self.object)
                messages.success(self.request, f"Examen '{self.object.nombre}' creado y preguntas asignadas correctamente.")
                return super().form_valid(form)
        except ValueError as e:
            # Si falla la asignación (por falta de preguntas), cancelamos la creación
            form.add_error('cantidad_preguntas', str(e))
            return self.form_invalid(form)

class ExamenUpdateView(LoginRequiredMixin, TeacherRequiredMixin, UpdateView):
    model = Examen
    form_class = ExamenForm
    template_name = 'AppEvaluar/examen_form.html'
    success_url = reverse_lazy('evaluar:examen_dashboard')

    def form_valid(self, form):
        try:
            with transaction.atomic():
                # Al actualizar, si cambia el tema o la cantidad de preguntas, 
                # debemos re-asignar las preguntas.
                examen_previo = Examen.objects.get(pk=self.kwargs['pk'])
                tema_cambio = (examen_previo.tema != form.cleaned_data['tema'])
                cantidad_cambio = (examen_previo.cantidad_preguntas != form.cleaned_data['cantidad_preguntas'])
                
                self.object = form.save()
                
                if tema_cambio or cantidad_cambio:
                    # Liberar preguntas actuales
                    self.object.preguntas.update(examen_tema=None)
                    # Asignar nuevas
                    asignar_preguntas_aleatorias(self.object)
                    messages.success(self.request, f"Examen '{self.object.nombre}' actualizado. Se han re-asignado las preguntas debido a cambios en el tema o cantidad.")
                else:
                    messages.success(self.request, f"Examen '{self.object.nombre}' actualizado correctamente.")
                
                return super().form_valid(form)
        except ValueError as e:
            form.add_error('cantidad_preguntas', str(e))
            return self.form_invalid(form)

class ExamenDeleteView(LoginRequiredMixin, TeacherRequiredMixin, View):
    def post(self, request, pk):
        examen = get_object_or_404(Examen, pk=pk)
        nombre = examen.nombre
        examen.delete()
        messages.success(request, f"Examen '{nombre}' eliminado. Las preguntas asociadas han sido liberadas.")
        return redirect('evaluar:examen_dashboard')

class ReportesDocenteView(LoginRequiredMixin, TeacherRequiredMixin, ListView):
    model = ProgresoEstudiante
    template_name = 'AppEvaluar/reportes_docente.html'
    context_object_name = 'progresos'

    def get_queryset(self):
        queryset = ProgresoEstudiante.objects.all()
        
        grado = self.request.GET.get('grado')
        seccion = self.request.GET.get('seccion')
        nombre = self.request.GET.get('nombre')
        
        if grado:
            queryset = queryset.filter(grado=grado)
        if seccion:
            queryset = queryset.filter(seccion=seccion)
        if nombre:
            queryset = queryset.filter(usuario__username__icontains=nombre) | \
                       queryset.filter(usuario__first_name__icontains=nombre) | \
                       queryset.filter(usuario__last_name__icontains=nombre)
            
        return queryset.select_related('usuario', 'tema').order_by('-fecha_registro')[:50]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['temas'] = Tema.objects.all()
        
        grado = self.request.GET.get('grado', '')
        seccion = self.request.GET.get('seccion', '')
        nombre = self.request.GET.get('nombre', '')
        tema_id = self.request.GET.get('tema', '')
        fecha_inicio = self.request.GET.get('fecha_inicio', '')
        fecha_fin = self.request.GET.get('fecha_fin', '')
        
        # Obtener Resumen de Aula Inicial (Carga de pÃ¡gina)
        summary = get_classroom_performance_summary(
            grado=grado, seccion=seccion, 
            fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, 
            tema_id=tema_id
        )
        context['summary'] = summary
        
        # Preparar datos para Chart.js
        labels = list(summary['desempeno_por_tema'].keys())
        data = list(summary['desempeno_por_tema'].values())
        
        context['chart_data_json'] = json.dumps({
            'labels': labels,
            'datasets': [{
                'label': 'Dominio Promedio (%)',
                'data': data,
                'backgroundColor': 'rgba(74, 144, 226, 0.2)',
                'borderColor': 'rgba(74, 144, 226, 1)',
                'borderWidth': 2,
                'pointBackgroundColor': 'rgba(74, 144, 226, 1)'
            }]
        })

        # Listado de Estudiantes (HU26)
        from AppGestionUsuario.models import Profile
        estudiantes = Profile.objects.filter(rol='Estudiante').select_related('user').prefetch_related('user__metricas', 'logros')
        
        if grado:
            estudiantes = estudiantes.filter(grado=grado)
        if seccion:
            estudiantes = estudiantes.filter(seccion=seccion)
        if nombre:
            estudiantes = estudiantes.filter(user__username__icontains=nombre) | \
                          estudiantes.filter(nombres__icontains=nombre) | \
                          estudiantes.filter(apellidos__icontains=nombre)
        
        context['estudiantes'] = estudiantes.order_by('apellidos', 'nombres')
        
        # Filtros para el template
        context['filtro_grado'] = grado
        context['filtro_seccion'] = seccion
        context['filtro_nombre'] = nombre
        context['filtro_tema'] = tema_id
        context['filtro_fecha_inicio'] = fecha_inicio
        context['filtro_fecha_fin'] = fecha_fin
        
        return context

class ReportesDataJSONView(LoginRequiredMixin, TeacherRequiredMixin, ListView):
    """
    Endpoint JSON para obtener datos de reportes filtrados vía AJAX (HU27).
    """
    def get(self, request, *args, **kwargs):
        grado = request.GET.get('grado')
        seccion = request.GET.get('seccion')
        nombre = request.GET.get('nombre')
        tema_id = request.GET.get('tema')
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')

        # 1. Resumen de Aula
        summary = get_classroom_performance_summary(
            grado=grado, seccion=seccion, 
            fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, 
            tema_id=tema_id
        )

        # 2. Listado de Estudiantes
        from AppGestionUsuario.models import Profile
        estudiantes_qs = Profile.objects.filter(rol='Estudiante').select_related('user').prefetch_related('user__metricas', 'logros')
        
        if grado: estudiantes_qs = estudiantes_qs.filter(grado=grado)
        if seccion: estudiantes_qs = estudiantes_qs.filter(seccion=seccion)
        if nombre:
            estudiantes_qs = estudiantes_qs.filter(user__username__icontains=nombre) | \
                             estudiantes_qs.filter(nombres__icontains=nombre) | \
                             estudiantes_qs.filter(apellidos__icontains=nombre)

        from .services_metrics import calcular_riesgo_estudiante
        estudiantes_data = []
        for est in estudiantes_qs.order_by('apellidos', 'nombres'):
            metricas = MetricasEstudiante.objects.filter(usuario=est.user).first()
            # Calcular riesgo (HU46)
            riesgo = calcular_riesgo_estudiante(est.user, tema_id=tema_id)
            
            estudiantes_data.append({
                'nombre_completo': f"{est.nombres} {est.apellidos}",
                'username': est.user.username,
                'aula': f"{est.grado} {est.seccion}",
                'xp': est.puntos_acumulados,
                'nivel': est.nivel_estudiante,
                'precision': float(metricas.precision_general) if metricas else 0,
                'insignias_count': est.logros.count(),
                'nivel_riesgo': riesgo['nivel'],
                'color_riesgo': riesgo['color'],
                'motivo_riesgo': riesgo['mensaje']
            })

        # 3. Datos de Actividad Reciente (Progresos)
        progresos_qs = ProgresoEstudiante.objects.all().select_related('usuario', 'tema')
        if grado: progresos_qs = progresos_qs.filter(grado=grado)
        if seccion: progresos_qs = progresos_qs.filter(seccion=seccion)
        
        progresos_data = []
        for p in progresos_qs.order_by('-fecha_registro')[:50]:
            progresos_data.append({
                'estudiante': p.usuario.get_full_name() or p.usuario.username,
                'aula': f"{p.grado} {p.seccion}",
                'tema': p.tema.nombre,
                'actividad': p.tipo_actividad,
                'fecha': p.fecha_registro.strftime("%d/%m %H:%i")
            })

        return JsonResponse({
            'summary': summary,
            'estudiantes': estudiantes_data,
            'progresos': progresos_data,
            'chart_data': {
                'labels': list(summary['desempeno_por_tema'].keys()),
                'values': list(summary['desempeno_por_tema'].values())
            }
        })

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
        dificultad=nivel,
        es_activo=True
    ).prefetch_related('opciones').order_by('?')[:5]

    if not ejercicios.exists():
        messages.info(request, f"Aún no hay ejercicios de nivel {nivel} para el tema: {tema.nombre}")
        # Fallback: Si no hay del nivel, mostrar cualquiera del tema para no bloquear al alumno
        ejercicios = Ejercicio.objects.filter(tema=tema, es_activo=True).prefetch_related('opciones').order_by('?')[:5]
        
    if not ejercicios.exists():
        messages.info(request, f"Aún no hay ejercicios cargados para el tema: {tema.nombre}")
        return redirect('lista_temas')

    return render(request, 'AppEvaluar/practica_ejercicio.html', {
        'tema': tema,
        'ejercicios': ejercicios,
        'total': ejercicios.count()
    })

from .services_geometry import GeometryValidator
import json

@login_required
@student_required
def validar_respuesta(request):
    """
    Endpoint AJAX para validar la opción seleccionada y guardar el resultado.
    Soporta ejercicios estáticos (opciones) e interactivos (geometría).
    """
    if request.method != 'POST':
        return HttpResponseBadRequest("Método no permitido")

    ejercicio_id = request.POST.get('ejercicio_id')
    tiempo = request.POST.get('tiempo', 0)
    ejercicio = get_object_or_404(Ejercicio, id=ejercicio_id)

    es_correcto = False
    feedback_especifico = ""
    solucion_fantasma = None # Para HU45 Fase 4

    if ejercicio.es_interactiva:
        # Lógica Interactiva (HU45)
        datos_json = request.POST.get('datos_geometricos')
        if not datos_json:
            return JsonResponse({"error": "No se recibieron datos geométricos"}, status=400)
        
        datos_geo = json.loads(datos_json)
        meta = ejercicio.meta_geometria
        
        # Seleccionar método de validación según el tipo
        tipo = meta.get('tipo_ejercicio', 'construir_angulo')
        if tipo == 'construir_angulo':
            es_correcto, error = GeometryValidator.validar_angulo(datos_geo, meta)
        elif tipo == 'distancia_segmento':
            es_correcto, error = GeometryValidator.validar_distancia(datos_geo, meta)
        else:
            es_correcto = False
            error = 999
        
        feedback_especifico = "¡Geometría correcta!" if es_correcto else f"La construcción no es precisa (Error: {error:.1f}°/u)."
        # La solución fantasma se enviará en la Fase 4
    else:
        # Lógica Estándar (HU14)
        opcion_id = request.POST.get('opcion_id')
        opcion = get_object_or_404(OpcionEjercicio, id=opcion_id, ejercicio=ejercicio)
        es_correcto = opcion.es_correcta
        feedback_especifico = opcion.retroalimentacion or ("¡Correcto!" if es_correcto else "Sigue intentándolo.")

    explicacion_tecnica = ejercicio.explicacion_tecnica or ""
    feedback_completo = f"{feedback_especifico} {explicacion_tecnica}".strip()

    # Persistir el resultado
    resultado_ej = ResultadoEjercicio.objects.create(
        usuario=request.user,
        ejercicio=ejercicio,
        es_correcto=es_correcto,
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

    # HU42: Evaluar éxito de la recomendación para retroalimentar el SVM
    evaluar_exito_recomendacion(request.user, ejercicio.tema.nombre, es_correcto)

    # HU47: Actualizar ciclo de repetición espaciada si aplica
    from .services_spaced_repetition import actualizar_repaso_post_ejercicio
    actualizar_repaso_post_ejercicio(request.user, ejercicio.tema, es_correcto)

    # Capturar nivel previo para detectar cambio (HU23)
    nivel_previo = request.user.profile.nivel_estudiante

    # Asignar puntos e insignias por actividad (HU22 y HU24)
    puntos_ganados, nuevas_insignias = GamificationService.assign_points_exercise(
        request.user, 
        is_correct=es_correcto, 
        difficulty=ejercicio.dificultad
    )

    # Refrescar perfil para obtener puntos y nivel actualizados
    request.user.profile.refresh_from_db()
    nivel_actual = request.user.profile.nivel_estudiante

    # Formatear insignias para JSON
    insignias_data = [
        {'nombre': b.nombre, 'icono': b.icono_clase} for b in nuevas_insignias
    ]

    return JsonResponse({
        'es_correcto': es_correcto,
        'feedback': feedback_especifico,
        'explicacion_tecnica': explicacion_tecnica,
        'puntos_ganados': puntos_ganados,
        'total_puntos': request.user.profile.puntos_acumulados,
        'nivel_actual': nivel_actual,
        'subio_nivel': nivel_actual > nivel_previo,
        'nuevas_insignias': insignias_data,
        'meta_solucion': ejercicio.meta_geometria if not es_correcto and ejercicio.es_interactiva else None
    })

@login_required
@student_required
def rendir_examen(request, examen_id):
    examen = get_object_or_404(ExamenDiagnostico, id=examen_id)
    
    # Validar si el estudiante ya realizó el examen (HU06)
    if ResultadoDiagnostico.objects.filter(estudiante=request.user, examen=examen).exists():
        messages.error(request, "Ya has realizado este examen diagnóstico.")
        return redirect('evaluar:ver_resultados', examen_id=examen.id)

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
            
            # HU42: Captura de tiempo de respuesta
            tiempo_valor = request.POST.get(f'tiempo_pregunta_{pregunta.id}')
            tiempo_respuesta = float(tiempo_valor) if tiempo_valor else None
            
            if valor:
                respuesta = RespuestaUsuario(
                    usuario=request.user,
                    pregunta=pregunta,
                    tiempo_respuesta=tiempo_respuesta
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
        temas_evaluados = preguntas.values_list('tema__nombre', flat=True).distinct()
        for nombre_tema in temas_evaluados:
            if not nombre_tema: continue
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
        return redirect('evaluar:ver_resultados', examen_id=examen.id)
        
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
            tema = respuesta.pregunta.tema.nombre if respuesta.pregunta.tema else "Sin Tema"
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

class BancoPreguntasCreateView(LoginRequiredMixin, TeacherRequiredMixin, CreateView):
    model = Ejercicio
    form_class = EjercicioForm
    template_name = 'AppEvaluar/banco_preguntas_form.html'
    success_url = reverse_lazy('evaluar:banco_preguntas_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['opciones'] = OpcionEjercicioFormSet(self.request.POST)
        else:
            data['opciones'] = OpcionEjercicioFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        opciones = context['opciones']
        if opciones.is_valid():
            self.object = form.save()
            opciones.instance = self.object
            opciones.save()
            messages.success(self.request, "Pregunta registrada exitosamente en el banco.")
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class BancoPreguntasListView(LoginRequiredMixin, TeacherRequiredMixin, ListView):
    model = Ejercicio
    template_name = 'AppEvaluar/banco_preguntas_list.html'
    context_object_name = 'ejercicios'
    ordering = ['-fecha_creacion']

    def get_queryset(self):
        # Por defecto solo mostramos las activas
        queryset = Ejercicio.objects.filter(es_activo=True).select_related('tema')
        
        # Aplicar filtros si existen en GET
        tema_id = self.request.GET.get('tema')
        dificultad = self.request.GET.get('dificultad')
        
        if tema_id:
            queryset = queryset.filter(tema_id=tema_id)
        if dificultad:
            queryset = queryset.filter(dificultad=dificultad)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pasar los temas y niveles para los selectores del frontend
        context['temas'] = Tema.objects.all()
        context['dificultades'] = [d[0] for d in Ejercicio.DIFICULTAD_CHOICES]
        # Mantener valores seleccionados para el sticky de filtros
        context['filtro_tema'] = self.request.GET.get('tema', '')
        context['filtro_dificultad'] = self.request.GET.get('dificultad', '')
        return context

class BancoPreguntasUpdateView(LoginRequiredMixin, TeacherRequiredMixin, UpdateView):
    model = Ejercicio
    form_class = EjercicioForm
    template_name = 'AppEvaluar/banco_preguntas_edit.html'
    success_url = reverse_lazy('evaluar:banco_preguntas_list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['opciones'] = OpcionEjercicioFormSet(self.request.POST, instance=self.object)
        else:
            data['opciones'] = OpcionEjercicioFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        opciones = context['opciones']
        if opciones.is_valid():
            self.object = form.save()
            opciones.instance = self.object
            opciones.save()
            messages.success(self.request, "Pregunta actualizada correctamente.")
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class BancoPreguntasDeleteView(LoginRequiredMixin, TeacherRequiredMixin, UpdateView):
    """
    Vista para eliminación lógica (Soft Delete) de ejercicios.
    Usamos UpdateView para cambiar el estado 'es_activo' sin borrar físicamente.
    """
    model = Ejercicio
    fields = [] # No necesitamos campos del formulario, solo la acción POST
    template_name = 'AppEvaluar/banco_preguntas_list.html' # Fallback
    success_url = reverse_lazy('evaluar:banco_preguntas_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.es_activo = False
        self.object.save()
        messages.success(request, "Pregunta eliminada (desactivada) exitosamente del banco.")
        return redirect(self.get_success_url())

class ExportarReporteExcelView(LoginRequiredMixin, TeacherRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):
        grado = request.GET.get('grado')
        seccion = request.GET.get('seccion')
        nombre = request.GET.get('nombre')
        tema_id = request.GET.get('tema')
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')

        excel_file = generar_excel_reporte_docente(
            grado=grado, 
            seccion=seccion, 
            nombre=nombre, 
            tema_id=tema_id, 
            fecha_inicio=fecha_inicio, 
            fecha_fin=fecha_fin
        )

        response = HttpResponse(
            excel_file.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=Reporte_Analitico_Aula.xlsx'
        return response

class ImportarBancoPreguntasView(LoginRequiredMixin, TeacherRequiredMixin, View):
    def get(self, request):
        return render(request, 'AppEvaluar/importar_banco.html')

    def post(self, request):
        archivo = request.FILES.get('archivo')
        
        if not archivo:
            return render(request, 'AppEvaluar/importar_banco.html', {'error': 'No se subió ningún archivo.'})

        extension = archivo.name.split('.')[-1].lower()
        texto = ""
        if extension == 'pdf':
            texto = extraer_texto_pdf(archivo)
        elif extension == 'docx':
            texto = extraer_texto_docx(archivo)
        else:
            return render(request, 'AppEvaluar/importar_banco.html', {'error': 'Formato no soportado. Usa PDF o DOCX.'})

        if not texto.strip():
            return render(request, 'AppEvaluar/importar_banco.html', {'error': 'No se pudo extraer texto del archivo.'})

        resultado = analizar_preguntas_con_gemini(texto)
        
        if "error" in resultado:
            return render(request, 'AppEvaluar/importar_banco.html', {'error': resultado['error']})

        return render(request, 'AppEvaluar/confirmar_importacion.html', {'preguntas': resultado['preguntas']})

class ConfirmarImportacionView(LoginRequiredMixin, TeacherRequiredMixin, View):
    def post(self, request):
        total_preguntas = int(request.POST.get('total_preguntas', 0))
        preguntas_guardadas = 0
        
        with transaction.atomic():
            for i in range(total_preguntas):
                if request.POST.get(f'incluir_{i}'):
                    enunciado = request.POST.get(f'enunciado_{i}')
                    tema_nombre = request.POST.get(f'tema_{i}')
                    dificultad = request.POST.get(f'dificultad_{i}')
                    explicacion = request.POST.get(f'explicacion_{i}')
                    correcta_index = request.POST.get(f'correcta_index_{i}')
                    
                    # Obtener o crear tema
                    tema, _ = Tema.objects.get_or_create(nombre=tema_nombre)
                    
                    # Crear Ejercicio
                    ejercicio = Ejercicio.objects.create(
                        tema=tema,
                        texto=enunciado,
                        dificultad=dificultad,
                        explicacion_tecnica=explicacion
                    )
                    
                    # Crear Opciones
                    # Buscamos todas las claves que empiecen con opcion_{i}_
                    opciones_encontradas = [k for k in request.POST.keys() if k.startswith(f'opcion_{i}_')]
                    for k in opciones_encontradas:
                        opcion_texto = request.POST.get(k)
                        # El índice de la opción es la última parte de la clave (ej. opcion_0_1 -> 1)
                        idx = k.split('_')[-1]
                        OpcionEjercicio.objects.create(
                            ejercicio=ejercicio,
                            texto=opcion_texto,
                            es_correcta=(idx == correcta_index)
                        )
                    preguntas_guardadas += 1
        
        messages.success(request, f"Se han importado exitosamente {preguntas_guardadas} preguntas al banco.")
        return redirect('evaluar:banco_preguntas_list')
