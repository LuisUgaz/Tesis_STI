from django.test import TestCase, RequestFactory
from .models import ConfiguracionGlobal
from .context_processors import global_config

class GlobalConfigContextProcessorTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.config = ConfiguracionGlobal.objects.create(
            nombre_sistema='Tesis Especial',
            email_contacto='especial@test.com'
        )

    def test_context_processor_returns_config(self):
        """Verificar que el procesador de contexto inyecta la configuración global."""
        request = self.factory.get('/')
        context = global_config(request)
        self.assertIn('global_config', context)
        self.assertEqual(context['global_config'].nombre_sistema, 'Tesis Especial')

    def test_context_processor_handles_no_config(self):
        """Verificar que el procesador crea una configuración por defecto si no existe."""
        ConfiguracionGlobal.objects.all().delete()
        request = self.factory.get('/')
        context = global_config(request)
        self.assertIn('global_config', context)
        self.assertEqual(context['global_config'].nombre_sistema, 'Tesis STI')
