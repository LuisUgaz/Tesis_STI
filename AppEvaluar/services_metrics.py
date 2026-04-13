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

def get_classroom_performance_summary(grado=None, seccion=None):
    """
    Calcula mÃ©tricas agregadas para un aula (grado y secciÃ³n).
    Retorna un diccionario con promedios y desempeÃ±o por tema.
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

    # 2. Promedio de PrecisiÃ³n General
    metricas = MetricasEstudiante.objects.filter(usuario_id__in=user_ids)
    avg_precision = metricas.aggregate(models.Avg('precision_general'))['precision_general__avg'] or 0
    
    # 3. Promedio de Puntos (XP)
    avg_puntos = profiles.aggregate(models.Avg('puntos_acumulados'))['puntos_acumulados__avg'] or 0
    
    # 4. DesempeÃ±o Agregado por Tema
    desempeno_agregado = {}
    temas_count = {}
    
    for m in metricas:
        if m.dominio_por_tema:
            for tema, valor in m.dominio_por_tema.items():
                desempeno_agregado[tema] = desempeno_agregado.get(tema, 0) + valor
                temas_count[tema] = temas_count.get(tema, 0) + 1
                
    # Calcular promedios por tema
    resumen_temas = {
        tema: round(float(desempeno_agregado[tema]) / temas_count[tema], 2)
        for tema in desempeno_agregado
    }
    
    return {
        'total_estudiantes': total_estudiantes,
        'precision_promedio': round(float(avg_precision), 2),
        'puntos_promedio': round(float(avg_puntos), 2),
        'desempeno_por_tema': resumen_temas
    }
