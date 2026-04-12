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
