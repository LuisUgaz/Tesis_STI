from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile

class ProfileViewTests(TestCase):
    def setUp(self):
        # Crear Estudiante
        self.student_user = User.objects.create_user(username='estudiante', password='password123', email='est@test.com')
        self.student_profile = Profile.objects.create(
            user=self.student_user, 
            nombres='Juan', 
            apellidos='Pérez', 
            rol='Estudiante',
            grado='2do',
            seccion='A'
        )
        
        # Crear Docente
        self.teacher_user = User.objects.create_user(username='docente', password='password123', email='doc@test.com')
        self.teacher_profile = Profile.objects.create(
            user=self.teacher_user, 
            nombres='María', 
            apellidos='López', 
            rol='Docente'
        )

    def test_view_own_profile_student(self):
        """Un estudiante puede ver su propio perfil."""
        self.client.login(username='estudiante', password='password123')
        response = self.client.get(reverse('profile', kwargs={'username': 'estudiante'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan Pérez')
        self.assertContains(response, '2do A')

    def test_view_own_profile_teacher(self):
        """Un docente puede ver su propio perfil."""
        self.client.login(username='docente', password='password123')
        response = self.client.get(reverse('profile', kwargs={'username': 'docente'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'María López')
        # No debería mostrar grado/sección si no están definidos o no son para su rol
        # (Dependerá de la implementación de la plantilla)

    def test_access_other_profile_restricted(self):
        """Un usuario no puede ver el perfil de otro usuario."""
        self.client.login(username='estudiante', password='password123')
        # Intentar ver el perfil del docente
        response = self.client.get(reverse('profile', kwargs={'username': 'docente'}))
        # Debería dar 403 o redirigir
        self.assertEqual(response.status_code, 403)

    def test_anonymous_access_redirects(self):
        """Usuarios no autenticados son redirigidos al login."""
        response = self.client.get(reverse('profile', kwargs={'username': 'estudiante'}))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)
