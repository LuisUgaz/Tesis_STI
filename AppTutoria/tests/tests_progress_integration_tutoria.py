from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from AppTutoria.models import Tema, ContenidoTema, VideoTema, ProgresoEstudiante
from AppGestionUsuario.models import Profile
from AppEvaluar.models import RecomendacionEstudiante

class ProgressIntegrationTutoriaTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='student_tut', password='password123')
        self.profile = Profile.objects.create(
            user=self.user,
            nombres='Tutoria',
            apellidos='Student',
            grado='5to',
            seccion='B',
            rol='Estudiante'
        )
        self.tema = Tema.objects.create(nombre='Triángulos', slug='triangulos')
        self.contenido = ContenidoTema.objects.create(tema=self.tema, cuerpo_html='<p>Teoría</p>')
        self.video = VideoTema.objects.create(tema=self.tema, titulo='Video 1', archivo_video='test.mp4')
        
        # Debe estar recomendado para tener acceso
        RecomendacionEstudiante.objects.create(usuario=self.user, tema='Triángulos', metrica_desempeno=50.0)
        
        self.client = Client()
        self.client.login(username='student_tut', password='password123')

    def test_progress_registered_after_theory_view(self):
        """Prueba que se registre progreso al ver la teoría de un tema."""
        response = self.client.get(reverse('tutoria:tema_detalle', args=[self.tema.slug]), {'seccion': 'teoria'})
        self.assertEqual(response.status_code, 200)
        
        # Verificar que se creó el progreso
        progreso = ProgresoEstudiante.objects.filter(
            usuario=self.user,
            tema=self.tema,
            tipo_actividad='Teoría'
        ).first()
        
        self.assertIsNotNone(progreso)
        self.assertEqual(progreso.grado, '5to')
        self.assertEqual(progreso.seccion, 'B')

    def test_progress_registered_after_video_view(self):
        """Prueba que se registre progreso al visualizar un video."""
        response = self.client.post(reverse('tutoria:registrar_visualizacion'), {
            'video_id': self.video.id
        })
        self.assertEqual(response.status_code, 200)
        
        # Verificar que se creó el progreso
        progreso = ProgresoEstudiante.objects.filter(
            usuario=self.user,
            tema=self.tema,
            tipo_actividad='Video'
        ).first()
        
        self.assertIsNotNone(progreso)
        self.assertEqual(progreso.grado, '5to')
        self.assertEqual(progreso.seccion, 'B')
        self.assertEqual(progreso.referencia_id, self.video.id)
