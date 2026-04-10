from django.test import TestCase
from django.contrib.auth.models import User
from .models import Tema, VideoTema, VisualizacionVideo

class VisualizacionVideoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teststudent', password='password123')
        self.tema = Tema.objects.create(nombre="Triángulos", slug="triangulos")
        self.video = VideoTema.objects.create(
            tema=self.tema,
            titulo="Propiedades Básicas",
            archivo_video="test.mp4",
            orden=1
        )

    def test_visualizacion_video_creation(self):
        """Verifica que se registre la visualización correctamente."""
        visualizacion = VisualizacionVideo.objects.create(
            usuario=self.user,
            video=self.video,
            contador=1
        )
        self.assertEqual(visualizacion.usuario, self.user)
        self.assertEqual(visualizacion.video, self.video)
        self.assertEqual(visualizacion.contador, 1)
        self.assertIsNotNone(visualizacion.fecha_primera_vista)
        self.assertIsNotNone(visualizacion.fecha_ultima_vista)
        self.assertEqual(str(visualizacion), "teststudent vio Propiedades Básicas (1 veces)")
