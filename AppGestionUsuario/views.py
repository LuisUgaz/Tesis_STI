from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import FormView, DetailView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, ContactoForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from .models import MetricasEstudiante, Insignia
from django.core.mail import send_mail
from django.conf import settings

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        
        if user.profile.rol == 'Estudiante':
            # Obtener logros del usuario indexados por ID de insignia para acceso rápido
            logros_dict = {
                l.insignia_id: l.fecha_obtencion 
                for l in user.profile.logros.all()
            }
            
            insignias = list(Insignia.objects.all())
            
            for insignia in insignias:
                insignia.ganada = insignia.id in logros_dict
                insignia.fecha_logro = logros_dict.get(insignia.id)
            
            # Ordenamiento: Ganadas primero (recientes primero), luego bloqueadas
            insignias.sort(
                key=lambda x: (not x.ganada, -(x.fecha_logro.timestamp() if x.fecha_logro else 0))
            )
            
            context['insignias'] = insignias
            
        return context

class MiProgresoView(LoginRequiredMixin, StudentRequiredMixin, DetailView):
    model = MetricasEstudiante
    template_name = 'AppGestionUsuario/mi_progreso.html'
    context_object_name = 'metricas'

    def get_object(self, queryset=None):
        # Siempre obtener o crear las mÃ©tricas para el usuario actual
        metricas, created = MetricasEstudiante.objects.get_or_create(usuario=self.request.user)
        return metricas

class ContactoView(LoginRequiredMixin, View):
    template_name = 'AppGestionUsuario/contacto.html'

    def get(self, request, *args, **kwargs):
        initial = {
            'tema_id': request.GET.get('tema_id'),
            'ejercicio_id': request.GET.get('ejercicio_id')
        }
        form = ContactoForm(initial=initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ContactoForm(request.POST)
        if form.is_valid():
            asunto = form.cleaned_data['asunto']
            mensaje_cuerpo = form.cleaned_data['mensaje']
            tema_id = form.cleaned_data.get('tema_id')
            ejercicio_id = form.cleaned_data.get('ejercicio_id')
            
            # Cuerpo detallado
            cuerpo_completo = (
                f"Consulta enviada por: {request.user.get_full_name()} ({request.user.username})\n"
                f"Correo del estudiante: {request.user.email}\n\n"
                f"Mensaje:\n{mensaje_cuerpo}\n\n"
            )
            
            if tema_id:
                cuerpo_completo += f"Contexto: ID del Tema: {tema_id}\n"
            if ejercicio_id:
                cuerpo_completo += f"Contexto: ID del Ejercicio: {ejercicio_id}\n"
                
            send_mail(
                asunto,
                cuerpo_completo,
                settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@tesis-sti.com',
                [settings.DOCENTE_EMAIL_DESTINO],
                fail_silently=False,
            )
            
            messages.success(request, "Su consulta ha sido enviada correctamente al docente.")
            return redirect('home')
            
        return render(request, self.template_name, {'form': form})
