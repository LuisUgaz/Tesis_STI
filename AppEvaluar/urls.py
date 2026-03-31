from django.urls import path
from . import views

urlpatterns = [
    path('rendir/<int:examen_id>/', views.rendir_examen, name='rendir_examen'),
    path('resultados/<int:examen_id>/', views.ver_resultados, name='ver_resultados'),
]
