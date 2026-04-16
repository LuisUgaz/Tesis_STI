from django.test import TestCase
from django.contrib.auth.models import User
from .models import ExamenDiagnostico, Pregunta, Opcion, RespuestaUsuario
from AppTutoria.models import Tema

class RespuestaUsuarioTiempoTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teststudent', password='password123')
        self.tema = Tema.objects.create(nombre="Geometría", slug="geometria")
        self.examen = ExamenDiagnostico.objects.create(nombre="Examen Prueba", tiempo_limite=45)
        self.pregunta = Pregunta.objects.create(examen=self.examen, texto="Pregunta 1", tema=self.tema)
        self.opcion = Opcion.objects.create(pregunta=self.pregunta, texto="Opción 1", es_correcta=True)

    def test_respuesta_usuario_con_tiempo_respuesta(self):
        """Verifica que el modelo RespuestaUsuario acepte el campo tiempo_respuesta."""
        respuesta = RespuestaUsuario.objects.create(
            usuario=self.user,
            pregunta=self.pregunta,
            opcion_seleccionada=self.opcion,
            tiempo_respuesta=15.5
        )
        self.assertEqual(respuesta.tiempo_respuesta, 15.5)
