from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from AppGestionUsuario.models import Profile
from AppTutoria.models import Tema, VideoTema, ContenidoTema
from AppEvaluar.models import RecomendacionEstudiante

class TutoriaGamificationIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='tutstudent', password='password123')
        self.profile = Profile.objects.create(
            user=self.user, 
            nombres='Tut', 
            apellidos='Student', 
            rol='Estudiante',
            grado='5to',
            seccion='A'
        )
        self.tema = Tema.objects.create(nombre="Polígonos", slug="poligonos")
        self.contenido = ContenidoTema.objects.create(tema=self.tema, cuerpo_html="<p>Teoría</p>")
        self.video = VideoTema.objects.create(
            tema=self.tema, 
            titulo="Intro Polígonos", 
            archivo_video="test.mp4"
        )
        # Necesario para acceder a temas/videos
        RecomendacionEstudiante.objects.create(usuario=self.user, tema=self.tema.nombre, metrica_desempeno=50)

    def test_points_assigned_on_video_view(self):
        """Al registrar visualización de video, el perfil debe ganar 5 puntos."""
        self.client.login(username='tutstudent', password='password123')
        
        response = self.client.post(reverse('tutoria:registrar_visualizacion'), {
            'video_id': self.video.id
        })
        
        self.assertEqual(response.status_code, 200)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.puntos_acumulados, 5)

    def test_points_not_duplicated_on_same_video(self):
        """No se deben asignar puntos por ver el mismo video más de una vez."""
        self.client.login(username='tutstudent', password='password123')
        
        # Primera vista
        self.client.post(reverse('tutoria:registrar_visualizacion'), {'video_id': self.video.id})
        # Segunda vista
        self.client.post(reverse('tutoria:registrar_visualizacion'), {'video_id': self.video.id})
        
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.puntos_acumulados, 5)

    def test_points_assigned_on_theory_access(self):
        """Al acceder a la sección de teoría, el perfil debe ganar 5 puntos."""
        self.client.login(username='tutstudent', password='password123')
        
        # En tema_detalle, la teoría se registra si seccion == 'teoria'
        response = self.client.get(reverse('tutoria:tema_detalle', kwargs={'slug': self.tema.slug}), {
            'seccion': 'teoria'
        })
        
        self.assertEqual(response.status_code, 200)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.puntos_acumulados, 5)

    def test_points_not_duplicated_on_same_theory(self):
        """No se deben asignar puntos por acceder a la misma teoría más de una vez."""
        self.client.login(username='tutstudent', password='password123')
        
        # Primera vez
        self.client.get(reverse('tutoria:tema_detalle', kwargs={'slug': self.tema.slug}), {'seccion': 'teoria'})
        # Segunda vez
        self.client.get(reverse('tutoria:tema_detalle', kwargs={'slug': self.tema.slug}), {'seccion': 'teoria'})
        
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.puntos_acumulados, 5)
