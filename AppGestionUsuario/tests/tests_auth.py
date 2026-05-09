from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class AuthTests(TestCase):
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

    def test_login_success(self):
        """Prueba de inicio de sesión exitoso con credenciales válidas."""
        response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password
        })
        # Tras un login exitoso, Django LoginView redirige (302)
        self.assertEqual(response.status_code, 302)
        self.assertIn('_auth_user_id', self.client.session)

    def test_login_invalid_password(self):
        """Prueba de fallo al ingresar una contraseña incorrecta."""
        response = self.client.post(self.login_url, {
            'username': self.username,
            'password': 'WrongPassword123'
        })
        self.assertEqual(response.status_code, 200) # Re-renderiza el formulario
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_login_invalid_user(self):
        """Prueba de fallo al ingresar un usuario inexistente."""
        response = self.client.post(self.login_url, {
            'username': 'nonexistent',
            'password': self.password
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)
