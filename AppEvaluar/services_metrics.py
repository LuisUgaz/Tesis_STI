from AppGestionUsuario.models import MetricasEstudiante
from django.db import transaction, models
from .models import ResultadoEjercicio, ResultadoDiagnostico
from decimal import Decimal

def actualizar_metricas_estudiante(usuario, actividad_reciente=None):
    """
    Calcula y actualiza las mÃ©tricas de desempeÃ±o del estudiante.
    actividad_reciente puede ser una instancia de ResultadoEjercicio o ResultadoDiagnostico.
    """
    with transaction.atomic():
        metricas, created = MetricasEstudiante.objects.get_or_create(usuario=usuario)
        
        # 1. Procesar Resultados de Ejercicios (PrÃ¡ctica)
        resultados_ej = ResultadoEjercicio.objects.filter(usuario=usuario)
        total_ej = resultados_ej.count()
        
        if total_ej > 0:
            # PrecisiÃ³n General
            aciertos = resultados_ej.filter(es_correcto=True).count()
            metricas.precision_general = (Decimal(aciertos) / Decimal(total_ej)) * 100
            
            # Tiempo de Respuesta Promedio
            avg_tiempo = resultados_ej.aggregate(models.Avg('tiempo_empleado'))['tiempo_empleado__avg']
            if avg_tiempo is not None:
                metricas.tiempo_respuesta_promedio = Decimal(avg_tiempo)
            
            # Dominio por Tema
            dominio = {}
            temas_con_ej = resultados_ej.values_list('ejercicio__tema__nombre', flat=True).distinct()
            for tema_nombre in temas_con_ej:
                res_tema = resultados_ej.filter(ejercicio__tema__nombre=tema_nombre)
                total_tema = res_tema.count()
                aciertos_tema = res_tema.filter(es_correcto=True).count()
                # Guardamos como float en el JSON para fÃ¡cil serializaciÃ³n
                dominio[tema_nombre] = float(round((Decimal(aciertos_tema) / Decimal(total_tema)) * 100, 2))
            metricas.dominio_por_tema = dominio
        
        # 2. Rendimiento AcadÃ©mico (Promedio de puntajes de diagnÃ³stico)
        resultados_diag = ResultadoDiagnostico.objects.filter(estudiante=usuario)
        avg_puntaje = resultados_diag.aggregate(models.Avg('puntaje'))['puntaje__avg']
        if avg_puntaje is not None:
            metricas.rendimiento_academico = Decimal(avg_puntaje)
            
        metricas.save()
        return metricas

def get_classroom_performance_summary(grado=None, seccion=None, fecha_inicio=None, fecha_fin=None, tema_id=None):
    """
    Calcula mÃ©tricas agregadas para un aula (grado y secciÃ³n) con filtros de fecha y tema.
    """
    from AppGestionUsuario.models import Profile, MetricasEstudiante
    
    # 1. Filtrar perfiles por grado y secciÃ³n
    profiles = Profile.objects.filter(rol='Estudiante')
    if grado:
        profiles = profiles.filter(grado=grado)
    if seccion:
        profiles = profiles.filter(seccion=seccion)
    
    user_ids = profiles.values_list('user_id', flat=True)
    total_estudiantes = profiles.count()
    
    if total_estudiantes == 0:
        return {
            'total_estudiantes': 0,
            'precision_promedio': 0,
            'puntos_promedio': 0,
            'desempeno_por_tema': {}
        }

    # 2. Filtrar resultados de ejercicios segÃºn fechas y tema
    resultados = ResultadoEjercicio.objects.filter(usuario_id__in=user_ids)
    if fecha_inicio:
        resultados = resultados.filter(fecha_resolucion__date__gte=fecha_inicio)
    if fecha_fin:
        resultados = resultados.filter(fecha_resolucion__date__lte=fecha_fin)
    if tema_id:
        resultados = resultados.filter(ejercicio__tema_id=tema_id)

    # 3. Promedio de PrecisiÃ³n en el periodo/tema
    avg_precision = 0
    if resultados.exists():
        aciertos = resultados.filter(es_correcto=True).count()
        avg_precision = (Decimal(aciertos) / Decimal(resultados.count())) * 100
    
    # 4. Promedio de Puntos (XP) de los estudiantes filtrados
    avg_puntos = profiles.aggregate(models.Avg('puntos_acumulados'))['puntos_acumulados__avg'] or 0
    
    # 5. DesempeÃ±o Agregado por Tema
    # Si se filtrÃ³ por tema_id, solo devolveremos ese tema en el desglose
    desempeno_por_tema = {}
    
    if tema_id:
        from AppTutoria.models import Tema
        t_obj = Tema.objects.get(id=tema_id)
        desempeno_por_tema[t_obj.nombre] = round(float(avg_precision), 2)
    else:
        # AgregaciÃ³n general por todos los temas basada en los resultados filtrados por fecha
        temas_ids = resultados.values_list('ejercicio__tema_id', flat=True).distinct()
        for t_id in temas_ids:
            res_tema = resultados.filter(ejercicio__tema_id=t_id)
            aciertos_t = res_tema.filter(es_correcto=True).count()
            t_nombre = res_tema.first().ejercicio.tema.nombre
            desempeno_por_tema[t_nombre] = round((float(aciertos_t) / res_tema.count()) * 100, 2)
    
    return {
        'total_estudiantes': total_estudiantes,
        'precision_promedio': round(float(avg_precision), 2),
        'puntos_promedio': round(float(avg_puntos), 2),
        'desempeno_por_tema': desempeno_por_tema
    }
