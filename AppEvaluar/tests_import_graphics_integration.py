from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Ejercicio
from AppTutoria.models import Tema
from unittest.mock import patch

class ImportGraphicsIntegrationTest(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_superuser(username='teacher_graphics', password='password123')
        self.client = Client()
        self.client.login(username='teacher_graphics', password='password123')

    @patch('AppEvaluar.services_ia_graphics.procesar_imagen_automatica')
    def test_import_triggers_graphic_generation(self, mock_procesar):
        """Verificar que la confirmación de importación dispara la generación de gráficos."""
        mock_procesar.return_value = True
        
        # Simular los datos que envía el formulario de confirmación
        data = {
            'total_preguntas': '1',
            'incluir_0': 'on',
            'enunciado_0': 'Dibuja un círculo de radio 5.',
            'tema_0': 'Geometría Plana',
            'dificultad_0': 'Básico',
            'explicacion_0': 'Explicación',
            'correcta_index_0': '0',
            'opcion_0_0': 'Opción 1'
        }
        
        response = self.client.post(reverse('evaluar:confirmar_importacion'), data)
        
        self.assertEqual(response.status_code, 302) # Redirect tras éxito
        self.assertTrue(mock_procesar.called)
        
        # Verificar que el ejercicio se creó
        self.assertEqual(Ejercicio.objects.count(), 1)
        ej = Ejercicio.objects.first()
        self.assertEqual(ej.texto, 'Dibuja un círculo de radio 5.')
