from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from AppGestionUsuario.models import Profile
from AppEvaluar.models import RecomendacionEstudiante
from .models import Tema, VideoTema

class VideoViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='estudiante1', password='password123')
        self.profile = Profile.objects.create(user=self.user, rol='Estudiante')
        
        self.tema = Tema.objects.create(nombre="Triángulos", slug="triangulos")
        self.video = VideoTema.objects.create(
            tema=self.tema,
            titulo="Tutorial Triángulos",
            archivo_video="test.mp4",
            orden=1
        )
        
        # URL esperada
        self.url = reverse('video_list', kwargs={'slug': self.tema.slug})

    def test_video_list_access_denied_without_recommendation(self):
        """Un estudiante sin la recomendación del tema no debería acceder."""
        self.client.login(username='estudiante1', password='password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403) # Permission Denied

    def test_video_list_access_granted_with_recommendation(self):
        """Un estudiante con la recomendación del tema debería acceder."""
        RecomendacionEstudiante.objects.create(
            usuario=self.user,
            tema=self.tema.nombre,
            metrica_desempeno=50.0
        )
        self.client.login(username='estudiante1', password='password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tutorial Triángulos")
        self.assertTemplateUsed(response, 'AppTutoria/videos.html')
