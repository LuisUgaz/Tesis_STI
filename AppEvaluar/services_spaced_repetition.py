import math

from django.utils import timezone
from datetime import timedelta
from .models import RepasoProgramado

def calcular_siguiente_repaso(intervalo_actual, ef_actual, es_exito):
    """
    Implementa una versión simplificada del algoritmo SM-2 para repetición espaciada. (HU47)
    
    Reglas:
    - Éxito: 
        - Nuevo Intervalo = Intervalo anterior * EF
        - EF = EF + 0.1 (Max 3.0)
    - Fallo (Penalización Suave):
        - Nuevo Intervalo = Intervalo anterior * 0.5 (Min 1)
        - EF = EF - 0.2 (Min 1.3)
    """
    if es_exito:
        nuevo_intervalo = math.ceil(intervalo_actual * ef_actual)
        nuevo_ef = min(ef_actual + 0.1, 3.0)
    else:
        nuevo_intervalo = max(math.floor(intervalo_actual * 0.5), 1)
        nuevo_ef = max(ef_actual - 0.2, 1.3)
    
    return nuevo_intervalo, round(nuevo_ef, 2)

def programar_repaso_inicial(usuario, tema_obj):
    """
    Crea el primer registro de repaso para un tema recién dominado. (HU47)
    Intervalo inicial: 1 día.
    """
    repaso, created = RepasoProgramado.objects.get_or_create(
        estudiante=usuario,
        tema=tema_obj,
        defaults={
            'fecha_proximo_repaso': timezone.now() + timedelta(days=1),
            'intervalo': 1,
            'factor_facilidad': 2.5,
            'estado': True
        }
    )
    return repaso, created

def actualizar_repaso_post_ejercicio(usuario, tema_obj, es_exito):
    """
    Actualiza el estado de un repaso programado tras la resolución de un ejercicio. (HU47)
    Solo actúa si el tema está actualmente en ciclo de repaso para ese estudiante.
    """
    repaso = RepasoProgramado.objects.filter(estudiante=usuario, tema=tema_obj, estado=True).first()
    if repaso:
        nuevo_intervalo, nuevo_ef = calcular_siguiente_repaso(
            repaso.intervalo, 
            repaso.factor_facilidad, 
            es_exito
        )
        
        repaso.intervalo = nuevo_intervalo
        repaso.factor_facilidad = nuevo_ef
        repaso.fecha_proximo_repaso = timezone.now() + timedelta(days=nuevo_intervalo)
        repaso.save()
        return True
    return False
