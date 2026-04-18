from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from AppGestionUsuario.models import Profile
from AppEvaluar.models import RecomendacionEstudiante
from .models import Tema, VideoTema

class VideoIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        # 1. Crear usuario y perfil
        self.user = User.objects.create_user(username='alumno_test', password='password123')
        self.profile = Profile.objects.create(user=self.user, rol='Estudiante')
        
        # 2. Crear temas
        self.tema_rec = Tema.objects.create(nombre="Triángulos", slug="triangulos")
        self.tema_no_rec = Tema.objects.create(nombre="Ángulos", slug="angulos")
        
        # 3. Crear video para el tema recomendado
        self.video = VideoTema.objects.create(
            tema=self.tema_rec,
            titulo="Video de Triángulos",
            archivo_video="video.mp4",
            orden=1
        )
        
        # 4. Asignar recomendación
        RecomendacionEstudiante.objects.create(
            usuario=self.user,
            tema=self.tema_rec.nombre,
            metrica_desempeno=60.0
        )

    def test_full_video_flow(self):
        """Prueba el flujo completo: Login -> Detalle Tema -> Lista Videos."""
        # Login
        self.client.login(username='alumno_test', password='password123')
        
        # Acceder al detalle del tema recomendado (HU10/HU11)
        response_detalle = self.client.get(reverse('tutoria:tema_detalle', kwargs={'slug': self.tema_rec.slug}))
        self.assertEqual(response_detalle.status_code, 200)
        # Verificar que el enlace a videos esté presente en el sidebar (Fase 3)
        self.assertContains(response_detalle, reverse('tutoria:video_list', kwargs={'slug': self.tema_rec.slug}))
        
        # Acceder a la lista de videos (HU12)
        response_videos = self.client.get(reverse('tutoria:video_list', kwargs={'slug': self.tema_rec.slug}))
        self.assertEqual(response_videos.status_code, 200)
        self.assertContains(response_videos, "Video de Triángulos")
        
        # Intentar acceder a videos de un tema NO recomendado (Debe redirigir)
        response_prohibido = self.client.get(reverse('tutoria:video_list', kwargs={'slug': self.tema_no_rec.slug}))
        self.assertRedirects(response_prohibido, reverse('tutoria:lista_temas'))
