from django.urls import path
from . import views

app_name = 'tutoria'

urlpatterns = [
    path('temas/', views.lista_temas, name='lista_temas'),
    path('temas/<slug:slug>/', views.tema_detalle, name='tema_detalle'),
    path('temas/<slug:slug>/videos/', views.video_list, name='video_list'),
    path('videos/visualizar/', views.registrar_visualizacion, name='registrar_visualizacion'),
    path('teoria/actualizar-progreso/', views.actualizar_progreso_teoria, name='actualizar_progreso_teoria'),
    # Gestión de videos (Docente)
    path('gestion/videos/', views.VideoTemaListView.as_view(), name='video_gestion_list'),
    path('gestion/videos/nuevo/', views.VideoTemaCreateView.as_view(), name='video_registro_create'),
    path('gestion/videos/<int:pk>/eliminar/', views.VideoTemaDeleteView.as_view(), name='video_registro_delete'),
    ]
