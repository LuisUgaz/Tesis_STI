from django.test import TestCase
from django.contrib.auth.models import User
from .models import MetricasEstudiante

class MetricasEstudianteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teststudent', password='password123')

    def test_metricas_creation(self):
        metricas = MetricasEstudiante.objects.create(usuario=self.user)
        self.assertEqual(metricas.precision_general, 0.0)
        self.assertEqual(metricas.dominio_por_tema, {})
        self.assertEqual(str(metricas), f"MÃ©tricas de {self.user.username}")
