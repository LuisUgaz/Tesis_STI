from django.test import TestCase
from django.contrib.auth.models import User
from .models import Ejercicio, ResultadoEjercicio
from AppTutoria.models import Tema
from .services_metrics import calcular_riesgo_estudiante, TIEMPO_MIN_ADIVINANZA, TIEMPO_MAX_FRUSTRACION, MIN_REINTENTOS_FRUSTRACION

class RiskAlertsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='risk_student', password='password123')
        self.tema = Tema.objects.create(nombre="Triángulos", slug="triangulos")
        self.ejercicio = Ejercicio.objects.create(tema=self.tema, texto="Test Risk", dificultad='Básico')

    def test_detect_adivinanza(self):
        """Adivinanza: Tiempo < TIEMPO_MIN_ADIVINANZA e incorrecto."""
        ResultadoEjercicio.objects.create(
            usuario=self.user, ejercicio=self.ejercicio, es_correcto=False,
            tiempo_empleado=TIEMPO_MIN_ADIVINANZA - 1, feedback_mostrado="Feedback"
        )
        riesgo = calcular_riesgo_estudiante(self.user)
        self.assertEqual(riesgo['nivel'], 'medio')
        self.assertIn('adivinanza', riesgo['mensaje'].lower())

    def test_detect_frustracion(self):
        """Frustración: Tiempo > TIEMPO_MAX_FRUSTRACION y múltiples reintentos fallidos."""
        # 3 reintentos fallidos lentos -> Esto también dispara estancamiento (Prioridad ALTO)
        for _ in range(MIN_REINTENTOS_FRUSTRACION):
            ResultadoEjercicio.objects.create(
                usuario=self.user, ejercicio=self.ejercicio, es_correcto=False,
                tiempo_empleado=TIEMPO_MAX_FRUSTRACION + 1, feedback_mostrado="Feedback"
            )
        riesgo = calcular_riesgo_estudiante(self.user)
        self.assertEqual(riesgo['nivel'], 'alto') # Estancamiento tiene prioridad
        self.assertIn('estancamiento', riesgo['mensaje'].lower())

    def test_detect_estancamiento(self):
        """Estancamiento: Tendencia negativa en los últimos 3 intentos (Hierarchically higher than medium)."""
        # Crear 3 resultados fallidos recientes
        for _ in range(3):
            ResultadoEjercicio.objects.create(
                usuario=self.user, ejercicio=self.ejercicio, es_correcto=False,
                tiempo_empleado=20, feedback_mostrado="Feedback"
            )
        riesgo = calcular_riesgo_estudiante(self.user)
        self.assertEqual(riesgo['nivel'], 'alto')
        self.assertIn('estancamiento', riesgo['mensaje'].lower())
        self.assertEqual(riesgo['color'], 'red')

    def test_riesgo_bajo(self):
        """Riesgo bajo: Desempeño positivo."""
        ResultadoEjercicio.objects.create(
            usuario=self.user, ejercicio=self.ejercicio, es_correcto=True,
            tiempo_empleado=30, feedback_mostrado="Feedback"
        )
        riesgo = calcular_riesgo_estudiante(self.user)
        self.assertEqual(riesgo['nivel'], 'bajo')
        self.assertEqual(riesgo['color'], 'green')

    def test_detect_frustracion_pura(self):
        """Frustración: Tiempos largos e incorrectos, pero con un acierto que evita el estancamiento total."""
        # 1. Fallo lento
        ResultadoEjercicio.objects.create(
            usuario=self.user, ejercicio=self.ejercicio, es_correcto=False,
            tiempo_empleado=TIEMPO_MAX_FRUSTRACION + 1, feedback_mostrado="Feedback"
        )
        # 2. Acierto (Rompe racha de estancamiento de 3 fallos)
        ResultadoEjercicio.objects.create(
            usuario=self.user, ejercicio=self.ejercicio, es_correcto=True,
            tiempo_empleado=30, feedback_mostrado="Feedback"
        )
        # 3. Otros 2 fallos lentos (Total fallos lentos = 3)
        for _ in range(2):
            ResultadoEjercicio.objects.create(
                usuario=self.user, ejercicio=self.ejercicio, es_correcto=False,
                tiempo_empleado=TIEMPO_MAX_FRUSTRACION + 1, feedback_mostrado="Feedback"
            )
        
        riesgo = calcular_riesgo_estudiante(self.user)
        self.assertEqual(riesgo['nivel'], 'medio')
        self.assertIn('frustración', riesgo['mensaje'].lower())
