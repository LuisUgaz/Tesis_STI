from django.test import TestCase
from AppTutoria.models import Tema
from AppEvaluar.forms import ExamenForm

class ExamenFormTest(TestCase):
    def setUp(self):
        self.tema = Tema.objects.create(nombre="Geometría Plana")

    def test_examen_form_valid(self):
        """Probar que el formulario es válido con todos los campos."""
        data = {
            'nombre': 'Examen de Prueba',
            'tema': self.tema.id,
            'cantidad_preguntas': 10,
            'tiempo_limite': 45
        }
        form = ExamenForm(data=data)
        self.assertTrue(form.is_valid())

    def test_examen_form_missing_tema(self):
        """Probar que el formulario falla si falta el tema."""
        data = {
            'nombre': 'Examen sin tema',
            'cantidad_preguntas': 10,
            'tiempo_limite': 45
        }
        form = ExamenForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('tema', form.errors)

    def test_examen_form_nombre_unique(self):
        """Probar que el formulario valida la unicidad del nombre."""
        from AppEvaluar.models import Examen
        Examen.objects.create(
            nombre='Examen Existente',
            tema=self.tema,
            cantidad_preguntas=5,
            tiempo_limite=30
        )
        data = {
            'nombre': 'Examen Existente',
            'tema': self.tema.id,
            'cantidad_preguntas': 10,
            'tiempo_limite': 45
        }
        form = ExamenForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)
