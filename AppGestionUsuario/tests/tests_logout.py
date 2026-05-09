from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class LogoutTests(TestCase):
    def setUp(self):
        # Crear un usuario de prueba
        self.username = 'testuser'
        self.password = 'Password123!'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
            email='test@ejemplo.com'
        )
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.home_url = reverse('home')

    def test_logout_success(self):
        """Prueba de cierre de sesión exitoso."""
        # Iniciar sesión primero
        self.client.login(username=self.username, password=self.password)
        self.assertIn('_auth_user_id', self.client.session)

        # Realizar logout
        response = self.client.post(self.logout_url)
        
        # Verificar redirección al login (configurado en urls.py)
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.login_url, response.url)
        
        # Verificar que la sesión se destruyó
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_access_restricted_after_logout(self):
        """Verificar que el acceso a 'home' se restringe tras el logout."""
        self.client.login(username=self.username, password=self.password)
        self.client.post(self.logout_url)
        
        # Intentar acceder a home (debe estar protegido)
        response = self.client.get(self.home_url)
        
        # Esperamos que redirija al login (302)
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.login_url, response.url)
