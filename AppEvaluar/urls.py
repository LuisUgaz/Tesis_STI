from django.urls import path
from . import views

urlpatterns = [
    path('rendir/<int:examen_id>/', views.rendir_examen, name='rendir_examen'),
    path('resultados/<int:examen_id>/', views.ver_resultados, name='ver_resultados'),
    path('practica/iniciar/', views.iniciar_practica, name='iniciar_practica'),
    path('practica/validar/', views.validar_respuesta, name='validar_respuesta'),
    path('historial/', views.HistorialResultadosView.as_view(), name='historial_resultados'),
]
