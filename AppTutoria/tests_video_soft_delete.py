from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Tema, VideoTema
from AppGestionUsuario.models import Profile

class VideoTemaSoftDeleteTest(TestCase):
    def setUp(self):
        # Crear usuarios con perfiles
        self.docente_user = User.objects.create_user(username='docente', password='password123')
        self.docente_profile = Profile.objects.create(user=self.docente_user, rol='Docente', nombres='Doc', apellidos='Ente')
        
        self.estudiante_user = User.objects.create_user(username='estudiante', password='password123')
        self.estudiante_profile = Profile.objects.create(user=self.estudiante_user, rol='Estudiante', nombres='Estu', apellidos='Diante')
        
        self.tema = Tema.objects.create(nombre="Geometría Plana", slug="geometria-plana")
        self.video = VideoTema.objects.create(
            tema=self.tema,
            titulo="Video Activo",
            url_video="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            orden=1,
            es_activo=True
        )
        self.video_inactivo = VideoTema.objects.create(
            tema=self.tema,
            titulo="Video Inactivo",
            url_video="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            orden=2,
            es_activo=False
        )
        
        self.client = Client()

    def test_docente_can_soft_delete_video(self):
        """Verifica que un docente pueda desactivar un video mediante POST."""
        self.client.login(username='docente', password='password123')
        url = reverse('tutoria:video_registro_delete', kwargs={'pk': self.video.pk})
        response = self.client.post(url)
        
        self.video.refresh_from_db()
        self.assertFalse(self.video.es_activo)
        self.assertRedirects(response, reverse('tutoria:video_gestion_list'))

    def test_estudiante_cannot_soft_delete_video(self):
        """Verifica que un estudiante no tenga acceso a la vista de eliminación."""
        self.client.login(username='estudiante', password='password123')
        url = reverse('tutoria:video_registro_delete', kwargs={'pk': self.video.pk})
        response = self.client.post(url)
        
        self.video.refresh_from_db()
        self.assertTrue(self.video.es_activo)
        self.assertEqual(response.status_code, 403)

    def test_docente_list_view_only_shows_active_videos(self):
        """Verifica que la lista de gestión del docente solo muestre videos activos."""
        self.client.login(username='docente', password='password123')
        url = reverse('tutoria:video_gestion_list')
        response = self.client.get(url)
        
        self.assertContains(response, "Video Activo")
        self.assertNotContains(response, "Video Inactivo")

    def test_docente_list_view_has_delete_button(self):
        """Verifica que el botón de eliminar esté presente en la lista de gestión."""
        self.client.login(username='docente', password='password123')
        url = reverse('tutoria:video_gestion_list')
        response = self.client.get(url)
        
        # El botón de eliminar debería contener la URL de eliminación
        delete_url = reverse('tutoria:video_registro_delete', kwargs={'pk': self.video.pk})
        self.assertContains(response, delete_url)
