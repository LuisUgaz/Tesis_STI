from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile

class ProfileDifficultyTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='password123')

    def test_profile_has_difficulty_level_field(self):
        """Verifica que el modelo Profile tenga el campo nivel_dificultad_actual."""
        profile = Profile.objects.create(user=self.user, rol='Estudiante')
        # Esta prueba fallará si el campo no existe
        self.assertTrue(hasattr(profile, 'nivel_dificultad_actual'))
        self.assertEqual(profile.nivel_dificultad_actual, 'Básico')

    def test_difficulty_level_choices(self):
        """Verifica que el campo acepte los valores permitidos."""
        profile = Profile.objects.create(user=self.user, rol='Estudiante')
        profile.nivel_dificultad_actual = 'Intermedio'
        profile.save()
        self.assertEqual(profile.nivel_dificultad_actual, 'Intermedio')
        
        profile.nivel_dificultad_actual = 'Avanzado'
        profile.save()
        self.assertEqual(profile.nivel_dificultad_actual, 'Avanzado')
