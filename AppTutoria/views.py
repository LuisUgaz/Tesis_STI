from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from AppEvaluar.models import RecomendacionEstudiante
from .models import Tema

@login_required
def lista_temas(request):
    """
    Muestra la lista de temas geométricos obtenidos de la BD, resaltando el recomendado.
    """
    # Verificar que el usuario tenga el perfil de Estudiante
    if not hasattr(request.user, 'profile') or request.user.profile.rol != 'Estudiante':
        raise PermissionDenied

    # Lista de temas desde la base de datos
    temas_db = list(Tema.objects.all())
    
    # Obtener recomendación (HU08)
    recomendacion = RecomendacionEstudiante.objects.filter(usuario=request.user).first()
    
    # Lógica de reordenamiento basada en la recomendación
    if recomendacion:
        # Buscar el tema en la lista de temas_db que coincida con el nombre de la recomendación
        tema_recomendado_obj = next((t for t in temas_db if t.nombre == recomendacion.tema), None)
        
        if tema_recomendado_obj:
            # Reordenar: colocar el objeto tema recomendado al principio
            temas_db.remove(tema_recomendado_obj)
            temas_db.insert(0, tema_recomendado_obj)

    return render(request, 'AppTutoria/lista_temas.html', {
        'temas': temas_db,
        'recomendacion': recomendacion
    })
