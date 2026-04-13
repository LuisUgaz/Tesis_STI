from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from AppGestionUsuario.models import Profile
from AppTutoria.models import Tema, VideoTema

class VideoRegistrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Crear usuarios
        self.docente_user = User.objects.create_user(username='docente_v', password='password123')
        self.docente_profile = Profile.objects.create(user=self.docente_user, rol='Docente')
        
        self.estudiante_user = User.objects.create_user(username='estudiante_v', password='password123')
        self.estudiante_profile = Profile.objects.create(user=self.estudiante_user, rol='Estudiante')
        
        # Crear Tema
        self.tema = Tema.objects.create(nombre="Triángulos", slug="triangulos")
        
        try:
            self.url_create = reverse('video_registro_create')
        except:
            self.url_create = '/tutoria/videos/nuevo/'

    def test_acceso_restringido_a_docentes(self):
        """Solo los docentes deben poder acceder al formulario de registro de videos."""
        # Estudiante no tiene acceso
        self.client.login(username='estudiante_v', password='password123')
        response = self.client.get(self.url_create)
        self.assertEqual(response.status_code, 403)
        
        # Docente tiene acceso
        self.client.login(username='docente_v', password='password123')
        response = self.client.get(self.url_create)
        self.assertEqual(response.status_code, 200)

    def test_registro_exitoso_video_youtube(self):
        """Debe registrar un video correctamente y extraer la miniatura de YouTube."""
        self.client.login(username='docente_v', password='password123')
        
        data = {
            'titulo': 'Propiedades de los Triángulos',
            'descripcion': 'Video explicativo sobre suma de ángulos.',
            'tema': self.tema.id,
            'url_video': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'orden': 1
        }
        
        response = self.client.post(self.url_create, data)
        self.assertEqual(response.status_code, 302) # Redirección tras éxito
        
        video = VideoTema.objects.get(titulo=data['titulo'])
        self.assertEqual(video.tema, self.tema)
        # Verificar que se generó la URL de miniatura (ID: dQw4w9WgXcQ)
        self.assertIn('dQw4w9WgXcQ', video.url_miniatura)
        self.assertIn('img.youtube.com', video.url_miniatura)

    def test_rechazo_url_invalida(self):
        """El sistema debe rechazar URLs que no sean de YouTube o estén mal formadas."""
        self.client.login(username='docente_v', password='password123')
        
        data = {
            'titulo': 'Video Inválido',
            'tema': self.tema.id,
            'url_video': 'https://google.com',
            'orden': 1
        }
        
        response = self.client.post(self.url_create, data)
        self.assertEqual(response.status_code, 200) # Se mantiene en el form con error
        form = response.context['form']
        self.assertFormError(form, 'url_video', 'Debe ingresar una URL válida de YouTube.')
