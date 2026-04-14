from django.test import TestCase
from .forms import ConfiguracionGlobalForm, PaginaEstaticaForm

class ConfiguracionGlobalFormTest(TestCase):
    def test_form_fields(self):
        form = ConfiguracionGlobalForm()
        self.assertIn('nombre_sistema', form.fields)
        self.assertIn('email_contacto', form.fields)
        self.assertIn('texto_footer', form.fields)

    def test_valid_data(self):
        data = {
            'nombre_sistema': 'Nuevo Sistema',
            'email_contacto': 'admin@test.com',
            'texto_footer': 'Pie de página'
        }
        form = ConfiguracionGlobalForm(data=data)
        self.assertTrue(form.is_valid())

class PaginaEstaticaFormTest(TestCase):
    def test_form_fields(self):
        form = PaginaEstaticaForm()
        self.assertIn('titulo', form.fields)
        self.assertIn('slug', form.fields)
        self.assertIn('contenido_html', form.fields)

    def test_valid_data(self):
        data = {
            'titulo': 'Nueva Página',
            'slug': 'nueva-pagina',
            'contenido_html': '<p>Contenido</p>'
        }
        form = PaginaEstaticaForm(data=data)
        self.assertTrue(form.is_valid())
