from django.urls import path
from . import views

urlpatterns = [
    path('temas/', views.lista_temas, name='lista_temas'),
    path('tema/<slug:slug>/', views.tema_detalle, name='tema_detalle'),
]
