from django.test import TestCase
from django.contrib.auth.models import User
from AppTutoria.models import Tema
from AppEvaluar.models import ExamenDiagnostico, Pregunta, Opcion, RespuestaUsuario
from AppEvaluar.services import obtener_feedback_ia
from unittest.mock import patch, MagicMock

class IAFeedbackServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teststudent', password='password')
        self.tema = Tema.objects.create(nombre="Geometría Plana")
        self.examen = ExamenDiagnostico.objects.create(nombre="Examen Test", tiempo_limite=45)
        
        self.pregunta = Pregunta.objects.create(
            texto="¿Cuánto suman los ángulos internos de un triángulo?",
            tema=self.tema,
            examen=self.examen,
            tipo='OPCION_MULTIPLE',
            dificultad='Básico'
        )
        
        self.opcion_correcta = Opcion.objects.create(
            pregunta=self.pregunta,
            texto="180°",
            es_correcta=True
        )
        self.opcion_incorrecta = Opcion.objects.create(
            pregunta=self.pregunta,
            texto="90°",
            es_correcta=False
        )
        
        self.respuesta = RespuestaUsuario.objects.create(
            usuario=self.user,
            pregunta=self.pregunta,
            opcion_seleccionada=self.opcion_incorrecta
        )

    @patch('google.generativeai.GenerativeModel.generate_content')
    def test_obtener_feedback_ia_success(self, mock_generate):
        """Verificar que el servicio devuelve la respuesta de la IA correctamente."""
        # Configurar el mock
        mock_response = MagicMock()
        mock_response.text = "La suma de los ángulos de un triángulo es 180°. Revisa la propiedad fundamental."
        mock_generate.return_value = mock_response
        
        feedback = obtener_feedback_ia(self.respuesta)
        
        self.assertEqual(feedback, mock_response.text)
        self.assertTrue(mock_generate.called)

    @patch('google.generativeai.GenerativeModel.generate_content')
    def test_obtener_feedback_ia_error(self, mock_generate):
        """Verificar el comportamiento cuando falla la API de IA."""
        mock_generate.side_effect = Exception("API Error")
        
        feedback = obtener_feedback_ia(self.respuesta)
        
        self.assertEqual(feedback, "No se pudo generar la explicacion IA")
