from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from AppGestionUsuario.models import Profile
from AppEvaluar.models import RecomendacionEstudiante
from .models import Tema, VideoTema, VisualizacionVideo
from .admin import VisualizacionVideoAdmin
from django.contrib.admin.sites import AdminSite

class VideoTrackingIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Student with Grade/Section
        self.user = User.objects.create_user(username='student_final', password='password123')
        self.profile = Profile.objects.create(
            user=self.user, 
            rol='Estudiante',
            grado='2',
            seccion='A'
        )
        
        self.tema = Tema.objects.create(nombre="Geometría", slug="geometria")
        self.video = VideoTema.objects.create(
            tema=self.tema,
            titulo="Video Final",
            archivo_video="final.mp4",
            orden=1
        )
        
        # Recommendation
        RecomendacionEstudiante.objects.create(
            usuario=self.user,
            tema=self.tema.nombre,
            metrica_desempeno=70.0
        )

    def test_integration_flow_and_admin_representation(self):
        """Prueba flujo completo y representación en Admin."""
        self.client.login(username='student_final', password='password123')
        
        # 1. Simular evento 'ended' (llamada al endpoint)
        url = reverse('tutoria:registrar_visualizacion')
        response = self.client.post(url, {'video_id': self.video.id})
        self.assertEqual(response.status_code, 200)
        
        # 2. Verificar persistencia
        vis = VisualizacionVideo.objects.get(usuario=self.user, video=self.video)
        self.assertEqual(vis.contador, 1)
        
        # 3. Verificar métodos del Admin
        site = AdminSite()
        admin = VisualizacionVideoAdmin(VisualizacionVideo, site)
        
        self.assertEqual(admin.get_grado(vis), '2')
        self.assertEqual(admin.get_seccion(vis), 'A')
        self.assertEqual(str(vis), "student_final vio Video Final (1 veces)")
