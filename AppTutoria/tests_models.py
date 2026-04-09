from django.test import TestCase
from .models import Tema

class TemaModelTest(TestCase):
    def setUp(self):
        self.tema = Tema.objects.create(
            nombre="Triángulos",
            descripcion="Estudio de los triángulos y sus propiedades."
        )

    def test_tema_creation(self):
        """Verifica que el tema se cree correctamente."""
        self.assertEqual(self.tema.nombre, "Triángulos")
        self.assertEqual(self.tema.descripcion, "Estudio de los triángulos y sus propiedades.")

    def test_tema_str(self):
        """Verifica la representación en cadena del modelo Tema."""
        self.assertEqual(str(self.tema), "Triángulos")
