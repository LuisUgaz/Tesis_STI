from django.urls import path
from . import views

urlpatterns = [
    path('temas/', views.lista_temas, name='lista_temas'),
    path('temas/<slug:slug>/', views.tema_detalle, name='tema_detalle'),
    path('temas/<slug:slug>/videos/', views.video_list, name='video_list'),
    path('videos/visualizar/', views.registrar_visualizacion, name='registrar_visualizacion'),
    # Gestión de videos (Docente)
    path('gestion/videos/', views.VideoTemaListView.as_view(), name='video_gestion_list'),
    path('gestion/videos/nuevo/', views.VideoTemaCreateView.as_view(), name='video_registro_create'),
    ]
