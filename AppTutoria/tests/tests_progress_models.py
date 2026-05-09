from django.test import TestCase
from django.contrib.auth.models import User
from AppTutoria.models import Tema, ProgresoEstudiante
from AppGestionUsuario.models import Profile
from AppTutoria.services import registrar_progreso

class ProgresoEstudianteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teststudent', password='password123')
        self.profile = Profile.objects.create(
            user=self.user,
            nombres='Test',
            apellidos='Student',
            grado='5to',
            seccion='B'
        )
        
        self.tema = Tema.objects.create(nombre='Triángulos')

    def test_create_progreso_estudiante(self):
        """Prueba que se pueda crear un registro de progreso correctamente."""
        progreso = ProgresoEstudiante.objects.create(
            usuario=self.user,
            tema=self.tema,
            tipo_actividad='Ejercicio',
            grado=self.profile.grado,
            seccion=self.profile.seccion,
            referencia_id=1
        )
        self.assertEqual(progreso.usuario, self.user)
        self.assertEqual(progreso.tema, self.tema)
        self.assertEqual(progreso.tipo_actividad, 'Ejercicio')
        self.assertEqual(progreso.grado, '5to')
        self.assertEqual(progreso.seccion, 'B')
        self.assertEqual(progreso.referencia_id, 1)
        self.assertIsNotNone(progreso.fecha_registro)

    def test_string_representation(self):
        """Prueba la representación en string del modelo."""
        progreso = ProgresoEstudiante.objects.create(
            usuario=self.user,
            tema=self.tema,
            tipo_actividad='Video',
            grado='5to',
            seccion='B'
        )
        expected_str = f"{self.user.username} - {self.tema.nombre} - Video"
        self.assertEqual(str(progreso), expected_str)

class ProgresoServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teststudent2', password='password123')
        self.profile = Profile.objects.create(
            user=self.user,
            nombres='Test',
            apellidos='Student',
            grado='6to',
            seccion='A'
        )
        self.tema = Tema.objects.create(nombre='Ángulos')

    def test_registrar_progreso_service(self):
        """Prueba que el servicio registrar_progreso cree el registro con grado y sección automáticos."""
        progreso = registrar_progreso(
            usuario=self.user,
            tema=self.tema,
            tipo_actividad='Teoría'
        )
        self.assertEqual(progreso.usuario, self.user)
        self.assertEqual(progreso.tema, self.tema)
        self.assertEqual(progreso.tipo_actividad, 'Teoría')
        self.assertEqual(progreso.grado, '6to')
        self.assertEqual(progreso.seccion, 'A')
        self.assertEqual(ProgresoEstudiante.objects.count(), 1)

    def test_registrar_progreso_with_reference(self):
        """Prueba que el servicio registre correctamente el referencia_id."""
        progreso = registrar_progreso(
            usuario=self.user,
            tema=self.tema,
            tipo_actividad='Ejercicio',
            referencia_id=123
        )
        self.assertEqual(progreso.referencia_id, 123)
