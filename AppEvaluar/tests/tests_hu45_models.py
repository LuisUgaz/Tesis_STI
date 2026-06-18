from django.test import TestCase
from AppEvaluar.models import Ejercicio, Tema
from unittest.mock import patch, MagicMock

class EjercicioInteractivoModelTests(TestCase):
    def setUp(self):
        self.tema = Tema.objects.create(nombre="Triángulos", slug="triangulos")
        
    @patch('google.genai.Client')
    def test_crear_ejercicio_interactivo_exitoso(self, mock_client_class):
        """Verifica que se puede crear un ejercicio marcado como interactivo con meta_geometria."""
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_response = MagicMock()
        mock_response.text = '{"puntos": [], "datos": [], "meta": "", "teoremas_sugeridos": []}'
        mock_client.models.generate_content.return_value = mock_response

        meta = {
            "tipo_ejercicio": "construir_angulo",
            "objetivo": 90,
            "tolerancia": 2,
            "elementos_iniciales": {
                "puntos": [{"id": "A", "x": 0, "y": 0, "fixed": True}],
                "segmentos": []
            }
        }
        ejercicio = Ejercicio.objects.create(
            tema=self.tema,
            texto="Construye un ángulo recto.",
            es_interactiva=True,
            meta_geometria=meta
        )
        
        self.assertTrue(ejercicio.es_interactiva)
        self.assertEqual(ejercicio.meta_geometria["tipo_ejercicio"], "construir_angulo")
        self.assertEqual(ejercicio.meta_geometria["objetivo"], 90)

    @patch('google.genai.Client')
    def test_ejercicio_por_defecto_no_es_interactivo(self, mock_client_class):
        """Verifica que por defecto los ejercicios no son interactivos (compatibilidad)."""
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_response = MagicMock()
        mock_response.text = '{"puntos": [], "datos": [], "meta": "", "teoremas_sugeridos": []}'
        mock_client.models.generate_content.return_value = mock_response

        ejercicio = Ejercicio.objects.create(
            tema=self.tema,
            texto="Ejercicio estático normal."
        )
        self.assertFalse(ejercicio.es_interactiva)
        self.assertIsNone(ejercicio.meta_geometria)
