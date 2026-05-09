from django.test import TestCase
from AppEvaluar.models import Ejercicio, Tema

class EjercicioInteractivoModelTests(TestCase):
    def setUp(self):
        self.tema = Tema.objects.create(nombre="Triángulos", slug="triangulos")
        
    def test_crear_ejercicio_interactivo_exitoso(self):
        """Verifica que se puede crear un ejercicio marcado como interactivo con meta_geometria."""
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

    def test_ejercicio_por_defecto_no_es_interactivo(self):
        """Verifica que por defecto los ejercicios no son interactivos (compatibilidad)."""
        ejercicio = Ejercicio.objects.create(
            tema=self.tema,
            texto="Ejercicio estático normal."
        )
        self.assertFalse(ejercicio.es_interactiva)
        self.assertIsNone(ejercicio.meta_geometria)
