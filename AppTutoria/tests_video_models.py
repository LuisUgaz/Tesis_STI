from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Tema, VideoTema

class VideoTemaModelTest(TestCase):
    def setUp(self):
        self.tema = Tema.objects.create(
            nombre="Geometría Plana",
            slug="geometria-plana",
            descripcion="Introducción a la geometría plana."
        )
        # Mock de archivos para el video y miniatura
        self.video_file = SimpleUploadedFile("test_video.mp4", b"video_content", content_type="video/mp4")
        self.thumbnail_file = SimpleUploadedFile("test_thumb.jpg", b"thumb_content", content_type="image/jpeg")

    def test_video_tema_creation(self):
        """Verifica que el modelo VideoTema se cree correctamente."""
        video = VideoTema.objects.create(
            tema=self.tema,
            titulo="Introducción a Triángulos",
            archivo_video=self.video_file,
            miniatura=self.thumbnail_file,
            descripcion="Un video introductorio.",
            duracion="10:00",
            orden=1
        )
        self.assertEqual(video.titulo, "Introducción a Triángulos")
        self.assertEqual(video.tema, self.tema)
        self.assertEqual(video.orden, 1)
        self.assertEqual(str(video), "Introducción a Triángulos (Geometría Plana)")
