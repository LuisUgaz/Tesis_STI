from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from AppGestionUsuario.models import Profile
from AppEvaluar.models import RecomendacionEstudiante
from .models import Tema, VideoTema, VisualizacionVideo

class VideoTrackingViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='student1', password='password123')
        self.profile = Profile.objects.create(user=self.user, rol='Estudiante')
        
        self.tema = Tema.objects.create(nombre="Triángulos", slug="triangulos")
        self.video = VideoTema.objects.create(
            tema=self.tema,
            titulo="Propiedades",
            archivo_video="test.mp4",
            orden=1
        )
        
        # URL del endpoint
        self.url = reverse('tutoria:registrar_visualizacion')

    def test_registrar_visualizacion_anonymous(self):
        """Un usuario no autenticado no puede registrar vistas."""
        response = self.client.post(self.url, {'video_id': self.video.id})
        self.assertEqual(response.status_code, 302) # Redirección a login

    def test_registrar_visualizacion_no_permission(self):
        """Un estudiante sin recomendación del tema no puede registrar vistas."""
        self.client.login(username='student1', password='password123')
        response = self.client.post(self.url, {'video_id': self.video.id})
        self.assertEqual(response.status_code, 403)

    def test_registrar_visualizacion_success(self):
        """Un estudiante con recomendación registra y aumenta el contador."""
        # Asignar recomendación
        RecomendacionEstudiante.objects.create(
            usuario=self.user,
            tema=self.tema.nombre,
            metrica_desempeno=50.0
        )
        self.client.login(username='student1', password='password123')
        
        # Primera vez
        response = self.client.post(self.url, {'video_id': self.video.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['contador'], 1)
        
        # Segunda vez
        response = self.client.post(self.url, {'video_id': self.video.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['contador'], 2)
        
        vis = VisualizacionVideo.objects.get(usuario=self.user, video=self.video)
        self.assertEqual(vis.contador, 2)
