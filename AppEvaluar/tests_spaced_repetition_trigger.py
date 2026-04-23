from django.test import TestCase
from django.contrib.auth.models import User
from .models import Ejercicio, ResultadoEjercicio, RepasoProgramado
from AppTutoria.models import Tema
from .services_metrics import actualizar_metricas_estudiante

class SpacedRepetitionTriggerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='student_trigger', password='password123')
        self.tema = Tema.objects.create(nombre="Triángulos", slug="triangulos")
        self.ejercicios = [
            Ejercicio.objects.create(tema=self.tema, texto=f"E{i}", dificultad='Básico')
            for i in range(15)
        ]

    def test_mastery_trigger_creates_repaso(self):
        """Si el estudiante supera el umbral (90% y 10+ ej), se crea un repaso."""
        # Crear 11 resultados correctos
        for i in range(11):
            res = ResultadoEjercicio.objects.create(
                usuario=self.user, ejercicio=self.ejercicios[i], es_correcto=True,
                tiempo_empleado=20, feedback_mostrado="Ok"
            )
        
        # Llamar explícitamente a la actualización de métricas (que dispara el trigger)
        actualizar_metricas_estudiante(self.user)
        
        repaso = RepasoProgramado.objects.filter(estudiante=self.user, tema=self.tema).first()
        self.assertIsNotNone(repaso)
        self.assertEqual(repaso.intervalo, 1)
        self.assertEqual(repaso.factor_facilidad, 2.5)

    def test_low_accuracy_no_trigger(self):
        """Si la precisión es < 90%, no se crea repaso."""
        # 10 ejercicios, 8 correctos (80%)
        for i in range(8):
            ResultadoEjercicio.objects.create(
                usuario=self.user, ejercicio=self.ejercicios[i], es_correcto=True,
                tiempo_empleado=20, feedback_mostrado="Ok"
            )
        for i in range(8, 10):
            ResultadoEjercicio.objects.create(
                usuario=self.user, ejercicio=self.ejercicios[i], es_correcto=False,
                tiempo_empleado=20, feedback_mostrado="Fail"
            )
        
        actualizar_metricas_estudiante(self.user)
        repaso = RepasoProgramado.objects.filter(estudiante=self.user, tema=self.tema).first()
        self.assertIsNone(repaso)

    def test_insufficient_exercises_no_trigger(self):
        """Si ha resuelto < 10 ejercicios, no se crea repaso aunque la precisión sea 100%."""
        for i in range(5):
            ResultadoEjercicio.objects.create(
                usuario=self.user, ejercicio=self.ejercicios[i], es_correcto=True,
                tiempo_empleado=20, feedback_mostrado="Ok"
            )
        
        actualizar_metricas_estudiante(self.user)
        repaso = RepasoProgramado.objects.filter(estudiante=self.user, tema=self.tema).first()
        self.assertIsNone(repaso)
