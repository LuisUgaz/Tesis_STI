from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from AppEvaluar.models import RecomendacionEstudiante

@login_required
def lista_temas(request):
    """
    Muestra la lista de temas geométricos, resaltando el recomendado por el sistema.
    """
    # Lista base de temas (HU08)
    temas = ['Triángulos', 'Ángulos', 'Segmentos', 'Rectas', 'Geometría Plana']
    
    # Obtener recomendación (HU08)
    recomendacion = RecomendacionEstudiante.objects.filter(usuario=request.user).first()
    
    if recomendacion and recomendacion.tema in temas:
        # Reordenar: colocar el recomendado al principio
        temas.remove(recomendacion.tema)
        temas.insert(0, recomendacion.tema)

    return render(request, 'AppTutoria/lista_temas.html', {
        'temas': temas,
        'recomendacion': recomendacion
    })
