from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile

class ProfileGamificationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teststudent', password='password123')
        self.profile = Profile.objects.create(
            user=self.user,
            nombres='Test',
            apellidos='Student',
            rol='Estudiante'
        )

    def test_profile_puntos_acumulados_default(self):
        """Prueba que el perfil tenga el campo puntos_acumulados y que su valor por defecto sea 0"""
        self.assertTrue(hasattr(self.profile, 'puntos_acumulados'), "El perfil debería tener el campo 'puntos_acumulados'")
        self.assertEqual(self.profile.puntos_acumulados, 0, "El valor inicial de puntos debería ser 0")

    def test_profile_puntos_acumulados_update(self):
        """Prueba que se puedan actualizar los puntos acumulados"""
        self.profile.puntos_acumulados = 50
        self.profile.save()
        updated_profile = Profile.objects.get(id=self.profile.id)
        self.assertEqual(updated_profile.puntos_acumulados, 50)
