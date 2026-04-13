from django.test import TestCase
from django.contrib.auth.models import User
from AppGestionUsuario.models import Profile, MetricasEstudiante
from AppTutoria.models import Tema
from AppEvaluar.models import Ejercicio, ResultadoEjercicio
from AppEvaluar.services_metrics import get_classroom_performance_summary
from decimal import Decimal

class ClassroomMetricsTest(TestCase):
    def setUp(self):
        # 1. Crear Tema y Usuarios
        self.tema = Tema.objects.create(nombre="Ángulos", slug="angulos")
        
        # Estudiante 1 (5to A)
        self.user1 = User.objects.create_user(username='student1', password='pass')
        self.profile1 = Profile.objects.create(
            user=self.user1, rol='Estudiante', grado='5to', seccion='A', puntos_acumulados=100
        )
        self.metricas1 = MetricasEstudiante.objects.create(
            usuario=self.user1, precision_general=80.0, dominio_por_tema={"Ángulos": 80.0}
        )

        # Estudiante 2 (5to A)
        self.user2 = User.objects.create_user(username='student2', password='pass')
        self.profile2 = Profile.objects.create(
            user=self.user2, rol='Estudiante', grado='5to', seccion='A', puntos_acumulados=200
        )
        self.metricas2 = MetricasEstudiante.objects.create(
            usuario=self.user2, precision_general=60.0, dominio_por_tema={"Ángulos": 60.0}
        )

        # Estudiante 3 (5to B - Diferente sección)
        self.user3 = User.objects.create_user(username='student3', password='pass')
        self.profile3 = Profile.objects.create(
            user=self.user3, rol='Estudiante', grado='5to', seccion='B', puntos_acumulados=500
        )
        self.metricas3 = MetricasEstudiante.objects.create(
            usuario=self.user3, precision_general=100.0, dominio_por_tema={"Ángulos": 100.0}
        )

    def test_get_classroom_performance_summary(self):
        """Prueba que se calculen promedios correctos para una sección específica"""
        summary = get_classroom_performance_summary(grado='5to', seccion='A')
        
        # Promedio de precisión: (80 + 60) / 2 = 70
        self.assertEqual(float(summary['precision_promedio']), 70.0)
        
        # Promedio de puntos: (100 + 200) / 2 = 150
        self.assertEqual(summary['puntos_promedio'], 150.0)
        
        # Total estudiantes: 2
        self.assertEqual(summary['total_estudiantes'], 2)

    def test_get_topic_performance_summary(self):
        """Prueba la agregación de dominio por tema en el aula"""
        summary = get_classroom_performance_summary(grado='5to', seccion='A')
        
        # Dominio promedio en Ángulos: (80 + 60) / 2 = 70
        self.assertIn('Ángulos', summary['desempeno_por_tema'])
        self.assertEqual(summary['desempeno_por_tema']['Ángulos'], 70.0)
