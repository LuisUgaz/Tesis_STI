from django.test import TestCase
from django.contrib.auth.models import User
from .models import ExamenDiagnostico, Pregunta, Opcion, RespuestaUsuario, ResultadoDiagnostico

class EvaluarModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teststudent', password='password123')
        # El perfil se crea automáticamente si hay una señal, pero vamos a asegurarnos o crearlo si es necesario
        # En AppGestionUsuario/models.py hay un modelo Profile, pero no vimos señales
        from AppGestionUsuario.models import Profile
        self.profile = Profile.objects.create(user=self.user, nombres='Test', apellidos='Student', rol='Estudiante')

        self.examen = ExamenDiagnostico.objects.create(
            nombre="Examen Diagnóstico Inicial",
            descripcion="Evaluación de conocimientos básicos de geometría",
            tiempo_limite=45
        )

        self.pregunta_opcion = Pregunta.objects.create(
            examen=self.examen,
            texto="¿Cuánto suman los ángulos internos de un triángulo?",
            tipo='OPCION_MULTIPLE',
            categoria='Triángulos'
        )

        self.opcion_correcta = Opcion.objects.create(
            pregunta=self.pregunta_opcion,
            texto="180 grados",
            es_correcta=True
        )

        self.opcion_incorrecta = Opcion.objects.create(
            pregunta=self.pregunta_opcion,
            texto="90 grados",
            es_correcta=False
        )

        self.pregunta_texto = Pregunta.objects.create(
            examen=self.examen,
            texto="Define qué es un segmento.",
            tipo='TEXTO_CORTO',
            categoria='Segmentos'
        )

    def test_examen_diagnostico_creation(self):
        self.assertEqual(self.examen.nombre, "Examen Diagnóstico Inicial")
        self.assertEqual(str(self.examen), "Examen Diagnóstico Inicial")

    def test_pregunta_creation(self):
        self.assertEqual(self.pregunta_opcion.categoria, 'Triángulos')
        self.assertEqual(self.pregunta_opcion.tipo, 'OPCION_MULTIPLE')
        self.assertEqual(str(self.pregunta_opcion), "¿Cuánto suman los ángulos internos de un triángulo?")

    def test_opcion_creation(self):
        self.assertTrue(self.opcion_correcta.es_correcta)
        self.assertFalse(self.opcion_incorrecta.es_correcta)
        self.assertEqual(str(self.opcion_correcta), "180 grados")

    def test_respuesta_usuario_creation(self):
        respuesta = RespuestaUsuario.objects.create(
            usuario=self.user,
            pregunta=self.pregunta_opcion,
            opcion_seleccionada=self.opcion_correcta
        )
        self.assertEqual(respuesta.usuario.username, 'teststudent')
        self.assertEqual(respuesta.opcion_seleccionada.texto, "180 grados")

    def test_respuesta_usuario_texto_creation(self):
        respuesta = RespuestaUsuario.objects.create(
            usuario=self.user,
            pregunta=self.pregunta_texto,
            respuesta_texto="Es una porción de recta limitada por dos puntos."
        )
        self.assertEqual(respuesta.respuesta_texto, "Es una porción de recta limitada por dos puntos.")

    def test_resultado_diagnostico_creation(self):
        from .models import ResultadoDiagnostico
        resultado = ResultadoDiagnostico.objects.create(
            estudiante=self.user,
            examen=self.examen,
            puntaje=85.50
        )
        self.assertEqual(resultado.estudiante.username, 'teststudent')
        self.assertEqual(float(resultado.puntaje), 85.50)
        self.assertIsNotNone(resultado.fecha_realizacion)
