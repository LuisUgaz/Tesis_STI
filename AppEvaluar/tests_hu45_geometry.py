from django.test import TestCase
from AppEvaluar.services_geometry import GeometryValidator

class GeometryValidatorTests(TestCase):
    def test_validar_angulo_correcto(self):
        """Verifica que un ángulo dentro de la tolerancia se marque como correcto."""
        meta = {"objetivo": 90, "tolerancia": 2}
        # Coordenadas que forman un ángulo de 90 grados
        datos = {
            "puntos": {
                "A": {"x": 1, "y": 0},
                "B": {"x": 0, "y": 0}, # Vértice
                "C": {"x": 0, "y": 1}
            }
        }
        resultado, error = GeometryValidator.validar_angulo(datos, meta)
        self.assertTrue(resultado)
        self.assertLess(error, 2)

    def test_validar_angulo_incorrecto(self):
        """Verifica que un ángulo fuera de la tolerancia se marque como incorrecto."""
        meta = {"objetivo": 90, "tolerancia": 2}
        datos = {
            "puntos": {
                "A": {"x": 1, "y": 0},
                "B": {"x": 0, "y": 0},
                "C": {"x": 1, "y": 1} # 45 grados
            }
        }
        resultado, error = GeometryValidator.validar_angulo(datos, meta)
        self.assertFalse(resultado)
        self.assertAlmostEqual(error, 45, places=1)

    def test_validar_distancia_correcta(self):
        """Verifica la validación de la longitud de un segmento."""
        meta = {"objetivo": 5, "tolerancia": 0.5}
        datos = {
            "puntos": {
                "P1": {"x": 0, "y": 0},
                "P2": {"x": 3, "y": 4} # Distancia = 5
            }
        }
        resultado, error = GeometryValidator.validar_distancia(datos, meta)
        self.assertTrue(resultado)
