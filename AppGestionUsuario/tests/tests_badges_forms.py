from django.test import TestCase
from AppGestionUsuario.forms import InsigniaForm
from AppGestionUsuario.models import Insignia

class InsigniaFormTest(TestCase):
    def test_form_fields(self):
        """Verificar que el formulario tiene los campos esperados."""
        form = InsigniaForm()
        expected_fields = ['nombre', 'descripcion', 'icono_clase', 'tipo_regla', 'valor_requerido']
        self.assertEqual(list(form.fields.keys()), expected_fields)

    def test_valid_data(self):
        """Probar formulario con datos válidos."""
        data = {
            'nombre': 'Explorador Geométrico',
            'descripcion': 'Otorgada por ver 5 videos educativos.',
            'icono_clase': 'fas fa-eye',
            'tipo_regla': 'HITOS',
            'valor_requerido': 5
        }
        form = InsigniaForm(data=data)
        self.assertTrue(form.is_valid())

    def test_missing_required_fields(self):
        """Probar que el formulario falla si faltan campos obligatorios."""
        form = InsigniaForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)
        self.assertIn('descripcion', form.errors)
        self.assertIn('icono_clase', form.errors)
        self.assertIn('tipo_regla', form.errors)

    def test_duplicate_name(self):
        """Probar que el formulario detecta nombres duplicados."""
        Insignia.objects.create(
            nombre='Insignia Duplicada',
            descripcion='Desc',
            icono_clase='icon',
            tipo_regla='HITOS',
            valor_requerido=1
        )
        data = {
            'nombre': 'Insignia Duplicada',
            'descripcion': 'Otra desc',
            'icono_clase': 'another-icon',
            'tipo_regla': 'DOMINIO',
            'valor_requerido': 10
        }
        form = InsigniaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)
