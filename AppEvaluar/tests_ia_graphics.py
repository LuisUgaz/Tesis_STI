from django.test import TestCase
from .services_ia_graphics import validar_codigo_seguro, generar_codigo_grafico, ejecutar_grafico_y_guardar, procesar_imagen_automatica
from unittest.mock import patch, MagicMock

class IAGraphicsTest(TestCase):
    def test_validar_codigo_seguro_ok(self):
        """Código válido debe pasar la validación."""
        codigo = "import matplotlib.pyplot as plt\nplt.plot([1,2],[3,4])"
        self.assertTrue(validar_codigo_seguro(codigo))

    def test_validar_codigo_seguro_dangerous(self):
        """Código con comandos peligrosos debe ser rechazado."""
        codigo_os = "import os\nos.system('ls')"
        self.assertFalse(validar_codigo_seguro(codigo_os))
        
        codigo_exec = "exec('print(1)')"
        self.assertFalse(validar_codigo_seguro(codigo_exec))

    def test_validar_codigo_no_matplotlib(self):
        """Código que no importa matplotlib debe ser rechazado."""
        codigo = "print('Hola')"
        self.assertFalse(validar_codigo_seguro(codigo))

    @patch('google.generativeai.GenerativeModel.generate_content')
    def test_generar_codigo_grafico_success(self, mock_generate):
        """Verificar que el servicio limpia el formato markdown."""
        mock_response = MagicMock()
        mock_response.text = "```python\nimport matplotlib.pyplot as plt\n```"
        mock_generate.return_value = mock_response
        
        codigo = generar_codigo_grafico("Triángulo")
        self.assertEqual(codigo, "import matplotlib.pyplot as plt")

    def test_ejecutar_grafico_y_guardar_success(self):
        """Verificar que el código se ejecuta y guarda el SVG."""
        from AppTutoria.models import Tema
        from .models import Ejercicio
        
        tema = Tema.objects.create(nombre="Test", slug="test")
        ejercicio = Ejercicio.objects.create(tema=tema, texto="Test", dificultad='Básico')
        
        codigo = "import matplotlib.pyplot as plt\nplt.plot([0,1],[0,1])"
        success, error = ejecutar_grafico_y_guardar(codigo, ejercicio.id)
        
        self.assertTrue(success)
        self.assertIsNone(error)
        
        ejercicio.refresh_from_db()
        self.assertTrue(ejercicio.imagen.name.endswith('.svg'))

    @patch('AppEvaluar.services_ia_graphics.generar_codigo_grafico')
    def test_procesar_imagen_automatica_retry(self, mock_generar):
        """Verificar que la lógica de reintento funciona ante un error de ejecución."""
        from AppTutoria.models import Tema
        from .models import Ejercicio
        
        tema = Tema.objects.create(nombre="Retry", slug="retry")
        ejercicio = Ejercicio.objects.create(tema=tema, texto="Retry", dificultad='Básico')
        
        # Simular: 1er intento código erróneo, 2do intento código correcto
        mock_generar.side_effect = [
            "import matplotlib.pyplot as plt\nERROR_SYNTAX", 
            "import matplotlib.pyplot as plt\nplt.plot([0,1],[0,1])"
        ]
        
        from .services_ia_graphics import procesar_imagen_automatica
        result = procesar_imagen_automatica("Retry", ejercicio)
        
        self.assertTrue(result)
        self.assertEqual(mock_generar.call_count, 2)
