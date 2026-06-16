from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Ejercicio
from .services_ia_logic import generar_representacion_formal
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Ejercicio)
def automatizar_enriquecimiento_ejercicio(sender, instance, created, **kwargs):
    """
    Signal para generar automáticamente la lógica formal cuando se crea un ejercicio.
    """
    # Si es nuevo y no tiene meta_geometria
    if created and not instance.meta_geometria:
        try:
            logger.info(f"Signal disparada: Generando lógica para nuevo ejercicio {instance.id}")
            res = generar_representacion_formal(instance)
            if res:
                # Usamos update para evitar disparar el signal de nuevo en un bucle infinito
                Ejercicio.objects.filter(id=instance.id).update(meta_geometria=res)
                logger.info(f"Lógica formal guardada automáticamente para ejercicio {instance.id}")
        except Exception as e:
            logger.error(f"Error en signal de enriquecimiento: {e}")
