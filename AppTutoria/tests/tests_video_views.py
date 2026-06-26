from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from AppGestionUsuario.models import Profile
from AppEvaluar.models import ExamenDiagnostico, RecomendacionEstudiante, ResultadoDiagnostico
from AppTutoria.models import Tema, VideoTema

class VideoViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='estudiante1', password='password123')
        self.profile = Profile.objects.create(user=self.user, rol='Estudiante')
        self.admin_user = User.objects.create_user(username='admin_sistema', password='password123')
        Profile.objects.create(user=self.admin_user, rol='Administrador')
        examen = ExamenDiagnostico.objects.create(nombre="Diagnostico Inicial")
        ResultadoDiagnostico.objects.create(estudiante=self.user, examen=examen, puntaje=50.0)
        
        self.tema = Tema.objects.create(nombre="Triángulos", slug="triangulos")
        self.video = VideoTema.objects.create(
            tema=self.tema,
            titulo="Tutorial Triángulos",
            archivo_video="test.mp4",
            orden=1,
            es_activo=True
        )
        
        # URL esperada
        self.url = reverse('tutoria:video_list', kwargs={'slug': self.tema.slug})

    def test_video_list_access_denied_without_recommendation(self):
        """Un estudiante sin la recomendación del tema no debería acceder y ser redirigido."""
        ResultadoDiagnostico.objects.filter(estudiante=self.user).delete()
        self.client.login(username='estudiante1', password='password123')
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('tutoria:lista_temas'))

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
        self.assertContains(response, "Tutorial")
        self.assertTemplateUsed(response, 'AppTutoria/videos.html')

    def test_video_list_access_granted_for_admin(self):
        """Un administrador puede previsualizar videos sin recomendacion."""
        self.client.login(username='admin_sistema', password='password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tutorial")
        self.assertTrue(response.context['es_docente'])
