from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile, Insignia, LogroEstudiante

class BadgesViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='badgestudent', password='password123')
        self.profile = Profile.objects.create(
            user=self.user,
            nombres='Badge',
            apellidos='Student',
            rol='Estudiante'
        )
        # Las insignias iniciales ya existen por la migración de datos HU24
        self.b_welcome = Insignia.objects.get(nombre="Primeros Pasos")
        self.b_master = Insignia.objects.get(nombre="Maestro de Triángulos")
        
    def test_profile_view_badge_data(self):
        """Prueba que el contexto incluya datos detallados de insignias"""
        # Ganar una insignia
        logro = LogroEstudiante.objects.create(perfil=self.profile, insignia=self.b_welcome)
        
        self.client.login(username='badgestudent', password='password123')
        response = self.client.get(reverse('profile', kwargs={'username': 'badgestudent'}))
        
        self.assertEqual(response.status_code, 200)
        insignias = response.context['insignias']
        
        # Buscar la insignia ganada en la lista del contexto
        welcome_in_context = next(i for i in insignias if i.id == self.b_welcome.id)
        
        self.assertTrue(welcome_in_context.ganada)
        self.assertIsNotNone(welcome_in_context.fecha_logro)
        self.assertEqual(welcome_in_context.fecha_logro, logro.fecha_obtencion)

    def test_profile_view_badge_sorting(self):
        """Prueba que las insignias ganadas aparezcan primero"""
        # Ganar solo la segunda insignia
        LogroEstudiante.objects.create(perfil=self.profile, insignia=self.b_master)
        
        self.client.login(username='badgestudent', password='password123')
        response = self.client.get(reverse('profile', kwargs={'username': 'badgestudent'}))
        
        insignias = list(response.context['insignias'])
        
        # La primera en la lista debería ser la ganada
        self.assertTrue(insignias[0].ganada)
        self.assertEqual(insignias[0].id, self.b_master.id)
        
        # Al menos una de las siguientes no debería estar ganada (asumiendo que hay más)
        self.assertFalse(insignias[-1].ganada)

    def test_profile_view_privacy(self):
        """Prueba que un estudiante no pueda ver el perfil (ni las insignias) de otro"""
        other_user = User.objects.create_user(username='otherstudent', password='password123')
        Profile.objects.create(user=other_user, nombres='Other', apellidos='Student', rol='Estudiante')
        
        self.client.login(username='badgestudent', password='password123')
        
        # Intentar acceder al perfil de 'otherstudent'
        response = self.client.get(reverse('profile', kwargs={'username': 'otherstudent'}))
        
        # Según la vista ProfileView, esto debería lanzar PermissionDenied (403)
        self.assertEqual(response.status_code, 403)

