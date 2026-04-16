from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import ExamenDiagnostico, Pregunta, Opcion, RespuestaUsuario
from AppTutoria.models import Tema

class RendirExamenTiempoTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='teststudent', password='password123')
        self.client.login(username='teststudent', password='password123')
        
        # Necesario si hay Profile y decoradores student_required
        from AppGestionUsuario.models import Profile
        Profile.objects.create(user=self.user, rol='Estudiante', grado='2do', seccion='A')
        
        self.tema = Tema.objects.create(nombre="Geometría", slug="geometria")
        self.examen = ExamenDiagnostico.objects.create(nombre="Examen Prueba", tiempo_limite=45)
        self.pregunta = Pregunta.objects.create(examen=self.examen, texto="Pregunta 1", tema=self.tema)
        self.opcion = Opcion.objects.create(pregunta=self.pregunta, texto="Opción 1", es_correcta=True)

    def test_guardar_tiempo_respuesta_en_view(self):
        """Verifica que la vista rindir_examen guarde el campo tiempo_respuesta del POST."""
        url = reverse('evaluar:rendir_examen', args=[self.examen.id])
        
        # Simulamos el envío del formulario con el nuevo campo de tiempo
        data = {
            f'pregunta_{self.pregunta.id}': self.opcion.id,
            f'tiempo_pregunta_{self.pregunta.id}': '12.5'
        }
        
        response = self.client.post(url, data)
        
        # Verificamos que se haya guardado la respuesta con el tiempo correcto
        respuesta = RespuestaUsuario.objects.get(usuario=self.user, pregunta=self.pregunta)
        self.assertEqual(respuesta.tiempo_respuesta, 12.5)
