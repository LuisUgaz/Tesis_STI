from django.test import TestCase
from django.contrib.auth.models import User
from .models import Ejercicio, ResultadoEjercicio, RepasoProgramado
from AppTutoria.models import Tema
from .services_spaced_repetition import actualizar_repaso_post_ejercicio
from django.utils import timezone
from datetime import timedelta

class SpacedRepetitionCycleTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='student_cycle', password='password123')
        self.tema = Tema.objects.create(nombre="Triángulos", slug="triangulos")
        self.repaso = RepasoProgramado.objects.create(
            estudiante=self.user,
            tema=self.tema,
            fecha_proximo_repaso=timezone.now(),
            intervalo=1,
            factor_facilidad=2.5,
            estado=True
        )

    def test_update_repaso_on_success(self):
        """Si el estudiante acierta, el intervalo aumenta."""
        actualizar_repaso_post_ejercicio(self.user, self.tema, True)
        
        self.repaso.refresh_from_db()
        self.assertEqual(self.repaso.intervalo, 3) # 1 * 2.5 = 2.5 -> ceil = 3
        self.assertEqual(self.repaso.factor_facilidad, 2.6)
        self.assertTrue(self.repaso.fecha_proximo_repaso > timezone.now() + timedelta(days=2))

    def test_update_repaso_on_failure(self):
        """Si el estudiante falla, el intervalo disminuye."""
        # Configurar un intervalo mayor para ver la reducción
        self.repaso.intervalo = 10
        self.repaso.save()
        
        actualizar_repaso_post_ejercicio(self.user, self.tema, False)
        
        self.repaso.refresh_from_db()
        self.assertEqual(self.repaso.intervalo, 5) # 10 * 0.5 = 5
        self.assertEqual(self.repaso.factor_facilidad, 2.3)

    def test_no_update_if_not_in_repaso(self):
        """Si no hay un registro de repaso activo para ese tema, no hace nada."""
        tema2 = Tema.objects.create(nombre="Ángulos", slug="angulos")
        updated = actualizar_repaso_post_ejercicio(self.user, tema2, True)
        self.assertFalse(updated)
