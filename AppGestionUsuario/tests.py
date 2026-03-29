from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile
from .forms import UserRegistrationForm
from django.urls import reverse

class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='estudiante1',
            email='estudiante@ejemplo.com',
            password='password123'
        )

    def test_profile_creation(self):
        """Verificar que se puede crear un perfil asociado a un usuario."""
        profile = Profile.objects.create(
            user=self.user,
            nombres='Juan',
            apellidos='Pérez',
            grado='5to',
            seccion='A',
            rol='Estudiante'
        )
        self.assertEqual(profile.user.username, 'estudiante1')
        self.assertEqual(profile.nombres, 'Juan')
        self.assertEqual(profile.rol, 'Estudiante')

    def test_profile_str_representation(self):
        """Verificar la representación en cadena del perfil."""
        profile = Profile.objects.create(
            user=self.user,
            nombres='Juan',
            apellidos='Pérez',
            rol='Estudiante'
        )
        self.assertEqual(str(profile), 'Juan Pérez (estudiante1)')

class RegistrationFormTest(TestCase):
    def test_form_passwords_dont_match(self):
        """Verificar que el formulario falla si las contraseñas no coinciden."""
        data = {
            'username': 'testuser',
            'email': 'test@ejemplo.com',
            'password': 'Password123!',
            'confirm_password': 'DifferentPassword123!',
            'nombres': 'Test',
            'apellidos': 'User',
            'grado': '5to',
            'seccion': 'B'
        }
        form = UserRegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('confirm_password', form.errors)

    def test_form_valid_data(self):
        """Verificar que el formulario es válido con datos correctos."""
        data = {
            'username': 'testuser',
            'email': 'test@ejemplo.com',
            'password': 'Password123!',
            'confirm_password': 'Password123!',
            'nombres': 'Test',
            'apellidos': 'User',
            'grado': '5to',
            'seccion': 'B'
        }
        form = UserRegistrationForm(data=data)
        self.assertTrue(form.is_valid())

class RegisterViewTest(TestCase):
    def test_register_view_success(self):
        """Verificar que la vista de registro crea el usuario y el perfil."""
        data = {
            'username': 'newuser',
            'email': 'new@ejemplo.com',
            'password': 'Password123!',
            'confirm_password': 'Password123!',
            'nombres': 'Nuevo',
            'apellidos': 'Usuario',
            'grado': '4to',
            'seccion': 'C'
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302) # Redirección tras éxito
        self.assertTrue(User.objects.filter(username='newuser').exists())
        user = User.objects.get(username='newuser')
        self.assertTrue(Profile.objects.filter(user=user).exists())
        self.assertEqual(user.profile.grado, '4to')
