from django.test import TestCase
from django.contrib.auth.models import User
from AppTutoria.models import Tema
from AppEvaluar.models import Ejercicio, OpcionEjercicio, ResultadoEjercicio
from unittest.mock import patch, MagicMock

class EjercicioModelTest(TestCase):
    def setUp(self):
        self.tema = Tema.objects.create(nombre="Triángulos", slug="triangulos")
        self.user = User.objects.create_user(username='estudiante_test', password='password123')

    @patch('google.genai.Client')
    def test_ejercicio_creation(self, mock_client_class):
        """Verifica la creación de un ejercicio."""
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_response = MagicMock()
        mock_response.text = '{"puntos": ["A", "B", "C"], "datos": [], "meta": "Suma", "teoremas_sugeridos": []}'
        mock_client.models.generate_content.return_value = mock_response

        ejercicio = Ejercicio.objects.create(
            tema=self.tema,
            texto="¿Cuánto suman los ángulos internos de un triángulo?",
            dificultad='Básico'
        )
        self.assertEqual(ejercicio.texto, "¿Cuánto suman los ángulos internos de un triángulo?")
        self.assertEqual(ejercicio.tema, self.tema)
        self.assertEqual(ejercicio.dificultad, 'Básico')

    @patch('google.genai.Client')
    def test_opcion_ejercicio_creation(self, mock_client_class):
        """Verifica la creación de opciones para un ejercicio."""
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_response = MagicMock()
        mock_response.text = '{"puntos": [], "datos": [], "meta": "", "teoremas_sugeridos": []}'
        mock_client.models.generate_content.return_value = mock_response

        ejercicio = Ejercicio.objects.create(tema=self.tema, texto="Test", dificultad='Básico')
        opcion = OpcionEjercicio.objects.create(
            ejercicio=ejercicio,
            texto="180 grados",
            es_correcta=True,
            retroalimentacion="Correcto, la suma es 180."
        )
        self.assertEqual(opcion.texto, "180 grados")
        self.assertTrue(opcion.es_correcta)

    @patch('google.genai.Client')
    def test_resultado_ejercicio_creation(self, mock_client_class):
        """Verifica el registro de un resultado de ejercicio."""
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_response = MagicMock()
        mock_response.text = '{"puntos": [], "datos": [], "meta": "", "teoremas_sugeridos": []}'
        mock_client.models.generate_content.return_value = mock_response

        ejercicio = Ejercicio.objects.create(tema=self.tema, texto="Test", dificultad='Básico')
        resultado = ResultadoEjercicio.objects.create(
            usuario=self.user,
            ejercicio=ejercicio,
            es_correcto=True,
            tiempo_empleado=15,
            feedback_mostrado="Buen trabajo."
        )
        self.assertEqual(resultado.usuario, self.user)
        self.assertTrue(resultado.es_correcto)
        self.assertEqual(resultado.tiempo_empleado, 15)
