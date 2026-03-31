from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import ExamenDiagnostico, Pregunta, Opcion, RespuestaUsuario
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

def student_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request.user.profile.rol != 'Estudiante':
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func

@login_required
@student_required
def rendir_examen(request, examen_id):
    examen = get_object_or_404(ExamenDiagnostico, id=examen_id)
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
        
        # Eliminar respuestas previas
        RespuestaUsuario.objects.filter(usuario=request.user, pregunta__examen=examen).delete()
        
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
                    except (Opcion.DoesNotExist, ValueError):
                        continue
                else:
                    respuesta.respuesta_texto = valor
                
                respuesta.save()
        
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
    
    if not respuestas.exists():
        messages.warning(request, "No tienes resultados para este examen.")
        return redirect('home')

    total_preguntas = examen.preguntas.count()
    total_correctas = 0
    resumen_temas = {}

    for respuesta in respuestas:
        tema = respuesta.pregunta.categoria
        if tema not in resumen_temas:
            resumen_temas[tema] = {'correctas': 0, 'total': 0}
        
        resumen_temas[tema]['total'] += 1
        
        es_correcta = False
        if respuesta.pregunta.tipo == 'OPCION_MULTIPLE':
            if respuesta.opcion_seleccionada and respuesta.opcion_seleccionada.es_correcta:
                es_correcta = True
        else:
            # Para texto corto, la lógica de corrección es más compleja.
            pass
            
        if es_correcta:
            total_correctas += 1
            resumen_temas[tema]['correctas'] += 1

    # Calcular porcentajes por tema
    for tema, datos in resumen_temas.items():
        datos['porcentaje'] = round((datos['correctas'] / datos['total']) * 100, 2)

    puntaje_total = round((total_correctas / total_preguntas) * 20, 2) if total_preguntas > 0 else 0

    return render(request, 'AppEvaluar/resultados.html', {
        'examen': examen,
        'puntaje_total': puntaje_total,
        'total_correctas': total_correctas,
        'total_preguntas': total_preguntas,
        'resumen_temas': resumen_temas
    })
