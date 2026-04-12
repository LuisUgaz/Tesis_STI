from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView, DetailView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from .models import MetricasEstudiante

class StudentRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.profile.rol == 'Estudiante'
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("Solo los estudiantes pueden acceder a esta secciÃ³n.")
        return super().handle_no_permission()

class RegisterView(FormView):
    template_name = 'AppGestionUsuario/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Registro exitoso. Ahora puedes iniciar sesión.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error en el registro. Por favor, verifica los campos.")
        return super().form_invalid(form)

class CustomLoginView(LoginView):
    template_name = 'AppGestionUsuario/login.html'
    
    def form_valid(self, form):
        remember_me = self.request.POST.get('remember_me')
        if not remember_me:
            # La sesión expira al cerrar el navegador
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super().form_valid(form)

class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, "Has cerrado sesión exitosamente. ¡Vuelve pronto!")
        return super().dispatch(request, *args, **kwargs)

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'AppGestionUsuario/profile.html'
    context_object_name = 'profile_user'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        
        # Validar privacidad: solo el propio usuario puede ver su perfil
        if self.request.user != user:
            raise PermissionDenied("No tienes permiso para ver este perfil.")
        
        return user

class MiProgresoView(LoginRequiredMixin, StudentRequiredMixin, DetailView):
    model = MetricasEstudiante
    template_name = 'AppGestionUsuario/mi_progreso.html'
    context_object_name = 'metricas'

    def get_object(self, queryset=None):
        # Siempre obtener o crear las mÃ©tricas para el usuario actual
        metricas, created = MetricasEstudiante.objects.get_or_create(usuario=self.request.user)
        return metricas
