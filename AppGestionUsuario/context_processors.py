from .models import ConfiguracionGlobal

def global_config(request):
    """
    Inyecta la configuración global en todas las plantillas.
    Garantiza que siempre exista al menos una configuración por defecto.
    """
    config, created = ConfiguracionGlobal.objects.get_or_create()
    return {
        'global_config': config
    }
