from django.test import TestCase
from .models import ConfiguracionGlobal, PaginaEstatica

class ConfiguracionGlobalModelTest(TestCase):
    def test_singleton_creation(self):
        """Verificar que solo existe una instancia de ConfiguracionGlobal."""
        ConfiguracionGlobal.objects.create(
            nombre_sistema='Sistema Test',
            email_contacto='test@ejemplo.com',
            texto_footer='© 2026 Test'
        )
        # Intentar crear otra no debería ser posible o debería retornar la misma
        config, created = ConfiguracionGlobal.objects.get_or_create()
        self.assertEqual(ConfiguracionGlobal.objects.count(), 1)
        self.assertEqual(config.nombre_sistema, 'Sistema Test')

    def test_str_representation(self):
        config = ConfiguracionGlobal.objects.create(nombre_sistema='Tesis STI')
        self.assertEqual(str(config), 'Configuración Global - Tesis STI')

class PaginaEstaticaModelTest(TestCase):
    def test_pagina_creation(self):
        pagina = PaginaEstatica.objects.create(
            titulo='Inicio',
            slug='inicio',
            contenido_html='<p>Bienvenido</p>'
        )
        self.assertEqual(pagina.titulo, 'Inicio')
        self.assertEqual(pagina.slug, 'inicio')

    def test_str_representation(self):
        pagina = PaginaEstatica.objects.create(titulo='Sobre Nosotros', slug='nosotros')
        self.assertEqual(str(pagina), 'Página: Sobre Nosotros')
