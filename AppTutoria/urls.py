from django.urls import path
from . import views

urlpatterns = [
    path('temas/', views.lista_temas, name='lista_temas'),
]
