from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Insignia, LogroEstudiante

class BadgesModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='badgestudent', password='password123')
        self.profile = Profile.objects.create(
            user=self.user,
            nombres='Badge',
            apellidos='Student',
            rol='Estudiante'
        )
        # La insignia se creará en la fase verde
        
    def test_insignia_creation(self):
        """Prueba la creación de una insignia"""
        insignia = Insignia.objects.create(
            nombre="Insignia Única Test",
            descripcion="Descripción de prueba",
            tipo_regla="HITOS",
            icono_clase="fa-star"
        )
        self.assertEqual(str(insignia), "Insignia Única Test")

    def test_logro_estudiante_assignment(self):
        """Prueba la asignación de una insignia a un estudiante"""
        insignia = Insignia.objects.create(
            nombre="Explorador Único",
            descripcion="Viste 3 videos educativos",
            tipo_regla="HITOS",
            icono_clase="fa-eye"
        )
        logro = LogroEstudiante.objects.create(
            perfil=self.profile,
            insignia=insignia
        )
        self.assertEqual(self.profile.logros.count(), 1)
        self.assertEqual(self.profile.logros.first().insignia.nombre, "Explorador Único")
