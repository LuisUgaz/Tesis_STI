from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile, ConfiguracionGlobal, PaginaEstatica

class AdminContentDashboardViewTest(TestCase):
    def setUp(self):
        # Crear usuarios con diferentes roles
        self.admin_user = User.objects.create_user(username='admin', password='password123')
        Profile.objects.create(user=self.admin_user, rol='Administrador', nombres='Admin', apellidos='User')
        
        self.estudiante_user = User.objects.create_user(username='estudiante', password='password123')
        Profile.objects.create(user=self.estudiante_user, rol='Estudiante', nombres='Est', apellidos='User')

    def test_access_restricted_to_admin(self):
        """Verificar que solo administradores pueden acceder al dashboard de contenidos."""
        url = reverse('admin_content_dashboard')
        
        # Anónimo
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302) # Redirige al login
        
        # Estudiante
        self.client.login(username='estudiante', password='password123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403) # Prohibido
        
        # Administrador
        self.client.login(username='admin', password='password123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_context(self):
        """Verificar que el dashboard muestra la configuración y las páginas."""
        PaginaEstatica.objects.create(titulo='Inicio', slug='inicio')
        self.client.login(username='admin', password='password123')
        response = self.client.get(reverse('admin_content_dashboard'))
        self.assertIn('config', response.context)
        self.assertIn('paginas', response.context)
        self.assertEqual(len(response.context['paginas']), 1)
