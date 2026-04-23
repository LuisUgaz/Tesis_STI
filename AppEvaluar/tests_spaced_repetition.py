from django.test import TestCase
from .services_spaced_repetition import calcular_siguiente_repaso

class SpacedRepetitionLogicTest(TestCase):
    def test_interval_increase_on_success(self):
        """Acierto: El intervalo debe aumentar (Intervalo * EF)."""
        intervalo, ef = calcular_siguiente_repaso(1, 2.5, True)
        self.assertEqual(intervalo, 3) # math.ceil(1 * 2.5) = 3
        self.assertEqual(ef, 2.6) # 2.5 + 0.1

    def test_interval_decrease_on_failure(self):
        """Fallo: El intervalo debe reducirse a la mitad y el EF disminuir."""
        # Penalización suave: Intervalo * 0.5
        intervalo, ef = calcular_siguiente_repaso(10, 2.5, False)
        self.assertEqual(intervalo, 5) # 10 * 0.5
        self.assertEqual(ef, 2.3) # 2.5 - 0.2

    def test_ef_min_max_limits(self):
        """El EF no debe bajar de 1.3 ni subir de 3.0."""
        # Test max limit
        _, ef_max = calcular_siguiente_repaso(1, 3.0, True)
        self.assertEqual(ef_max, 3.0)
        
        # Test min limit
        _, ef_min = calcular_siguiente_repaso(1, 1.3, False)
        self.assertEqual(ef_min, 1.3)

    def test_min_interval(self):
        """El intervalo mínimo debe ser 1 día."""
        intervalo, _ = calcular_siguiente_repaso(1, 1.3, False)
        self.assertEqual(intervalo, 1)
