from django.urls import path
from .views import RegisterView, CustomLoginView, ProfileView, MiProgresoView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('mi-progreso/', MiProgresoView.as_view(), name='mi_progreso'),
]
