from django.test import TestCase
from unittest.mock import patch, MagicMock
from AppEvaluar.models import Ejercicio
from AppTutoria.models import Tema
from AppEvaluar.services_ia_logic import generar_representacion_formal

class EnriquecimientoIAMockTest(TestCase):
    def setUp(self):
        self.tema = Tema.objects.create(nombre="Geometría Analítica", slug="geometria-analitica")

    @patch('google.genai.Client')
    def test_generar_representacion_formal_mock_success(self, mock_client_class):
        """
        Prueba que generar_representacion_formal funciona correctamente con una respuesta
        exitosa mockeada del SDK moderno de Gemini, simulando structured outputs.
        """
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.text = '{"puntos": ["A", "B"], "datos": ["AB = 5"], "meta": "Calcular la pendiente", "teoremas_sugeridos": ["Distancia entre dos puntos"]}'
        mock_client.models.generate_content.return_value = mock_response
        
        ejercicio = Ejercicio.objects.create(
            tema=self.tema,
            texto="Dado los puntos A y B, calcula la pendiente si AB = 5.",
            meta_geometria=None
        )
        
        res = generar_representacion_formal(ejercicio)
        
        self.assertIsNotNone(res)
        self.assertEqual(res["puntos"], ["A", "B"])
        self.assertEqual(res["datos"], ["AB = 5"])
        self.assertEqual(res["meta"], "Calcular la pendiente")
