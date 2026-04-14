from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.views.generic import FormView, DetailView, ListView, CreateView, UpdateView
from django.db.models import Q
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, ContactoForm, AdminUserForm, ConfiguracionGlobalForm, PaginaEstaticaForm, InsigniaForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from .models import MetricasEstudiante, Insignia, Profile, ConfiguracionGlobal, PaginaEstatica
from django.core.mail import send_mail
from django.conf import settings

class StudentRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.profile.rol == 'Estudiante'
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("Solo los estudiantes pueden acceder a esta secciÃ³n.")
        return super().handle_no_permission()

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.profile.rol == 'Administrador'
    
    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("Acceso restringido: Solo los administradores pueden acceder a esta secciÃ³n.")
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
            
            # Obtener el email de destino de la configuración global
            config, _ = ConfiguracionGlobal.objects.get_or_create()
            email_destino = config.email_contacto
                
            send_mail(
                asunto,
                cuerpo_completo,
                settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@tesis-sti.com',
                [email_destino],
                fail_silently=False,
            )
            
            messages.success(request, "Su consulta ha sido enviada correctamente al docente.")
            return redirect('home')
            
        return render(request, self.template_name, {'form': form})

class UserManagementListView(AdminRequiredMixin, ListView):
    model = User
    template_name = 'AppGestionUsuario/admin_user_list.html'
    context_object_name = 'users'
    paginate_by = 20

    def get_queryset(self):
        queryset = User.objects.select_related('profile').all().order_by('-date_joined')
        
        # Filtros
        q = self.request.GET.get('q')
        rol = self.request.GET.get('rol')
        grado = self.request.GET.get('grado')
        seccion = self.request.GET.get('seccion')
        estado = self.request.GET.get('estado')

        if q:
            queryset = queryset.filter(
                Q(username__icontains=q) |
                Q(profile__nombres__icontains=q) |
                Q(profile__apellidos__icontains=q)
            )
        
        if rol:
            queryset = queryset.filter(profile__rol=rol)
        
        if grado:
            queryset = queryset.filter(profile__grado=grado)
            
        if seccion:
            queryset = queryset.filter(profile__seccion=seccion)
            
        if estado:
            is_active = estado == 'activo'
            queryset = queryset.filter(is_active=is_active)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pasar opciones para los filtros
        context['roles'] = [choice[0] for choice in Profile.ROLE_CHOICES]
        # Grados y secciones únicos del sistema
        context['grados'] = Profile.objects.exclude(grado=None).values_list('grado', flat=True).distinct()
        context['secciones'] = Profile.objects.exclude(seccion=None).values_list('seccion', flat=True).distinct()
        return context

class UserManagementCreateView(AdminRequiredMixin, CreateView):
    model = User
    form_class = AdminUserForm
    template_name = 'AppGestionUsuario/admin_user_form.html'
    success_url = reverse_lazy('admin_user_list')

    def form_valid(self, form):
        messages.success(self.request, f"Usuario {form.cleaned_data['username']} creado correctamente.")
        return super().form_valid(form)

class UserManagementUpdateView(AdminRequiredMixin, UpdateView):
    model = User
    form_class = AdminUserForm
    template_name = 'AppGestionUsuario/admin_user_form.html'
    success_url = reverse_lazy('admin_user_list')

    def form_valid(self, form):
        messages.success(self.request, f"Usuario {form.cleaned_data['username']} actualizado correctamente.")
        return super().form_valid(form)

class UserToggleStatusView(AdminRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        user.is_active = not user.is_active
        user.save()
        return JsonResponse({
            'status': 'active' if user.is_active else 'inactive',
            'username': user.username
        })

class AdminContentDashboardView(AdminRequiredMixin, ListView):
    model = PaginaEstatica
    template_name = 'AppGestionUsuario/admin_content_dashboard.html'
    context_object_name = 'paginas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        config, created = ConfiguracionGlobal.objects.get_or_create()
        context['config'] = config
        return context

class AdminConfigUpdateView(AdminRequiredMixin, UpdateView):
    model = ConfiguracionGlobal
    form_class = ConfiguracionGlobalForm
    template_name = 'AppGestionUsuario/admin_config_form.html'
    success_url = reverse_lazy('admin_content_dashboard')

    def get_object(self, queryset=None):
        config, created = ConfiguracionGlobal.objects.get_or_create()
        return config

    def form_valid(self, form):
        messages.success(self.request, "Configuración global actualizada correctamente.")
        return super().form_valid(form)

class AdminPaginaUpdateView(AdminRequiredMixin, UpdateView):
    model = PaginaEstatica
    form_class = PaginaEstaticaForm
    template_name = 'AppGestionUsuario/admin_pagina_form.html'
    success_url = reverse_lazy('admin_content_dashboard')

    def form_valid(self, form):
        messages.success(self.request, f"Página '{self.object.titulo}' actualizada correctamente.")
        return super().form_valid(form)

class HomeView(LoginRequiredMixin, DetailView):
    model = PaginaEstatica
    template_name = 'home_content.html'
    context_object_name = 'pagina'

    def get_object(self, queryset=None):
        pagina, created = PaginaEstatica.objects.get_or_create(
            slug='inicio',
            defaults={'titulo': 'Inicio', 'contenido_html': '<h3>Bienvenido al Tutor Inteligente de Geometría</h3><p>Explora los temas y mejora tus habilidades.</p>'}
        )
        return pagina

class BadgeManagementListView(AdminRequiredMixin, ListView):
    model = Insignia
    template_name = 'AppGestionUsuario/admin_badge_list.html'
    context_object_name = 'badges'

class BadgeManagementCreateView(AdminRequiredMixin, CreateView):
    model = Insignia
    form_class = InsigniaForm
    template_name = 'AppGestionUsuario/admin_badge_form.html'
    success_url = reverse_lazy('admin_badge_list')

    def form_valid(self, form):
        messages.success(self.request, f"Insignia '{form.cleaned_data['nombre']}' creada correctamente.")
        return super().form_valid(form)

class BadgeManagementUpdateView(AdminRequiredMixin, UpdateView):
    model = Insignia
    form_class = InsigniaForm
    template_name = 'AppGestionUsuario/admin_badge_form.html'
    success_url = reverse_lazy('admin_badge_list')

    def form_valid(self, form):
        messages.success(self.request, f"Insignia '{form.cleaned_data['nombre']}' actualizada correctamente.")
        return super().form_valid(form)

class BadgeManagementDeleteView(AdminRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        badge = get_object_or_404(Insignia, pk=pk)
        nombre = badge.nombre
        badge.delete()
        messages.success(request, f"Insignia '{nombre}' eliminada correctamente.")
        return redirect('admin_badge_list')
