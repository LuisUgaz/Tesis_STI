from django.test import TestCase
from django.contrib.auth.models import User
from AppTutoria.models import Tema
from .models import Ejercicio, OpcionEjercicio, ResultadoEjercicio

class EjercicioModelTest(TestCase):
    def setUp(self):
        self.tema = Tema.objects.create(nombre="Triángulos", slug="triangulos")
        self.user = User.objects.create_user(username='estudiante_test', password='password123')

    def test_ejercicio_creation(self):
        """Verifica la creación de un ejercicio."""
        ejercicio = Ejercicio.objects.create(
            tema=self.tema,
            texto="¿Cuánto suman los ángulos internos de un triángulo?",
            dificultad='Básico'
        )
        self.assertEqual(ejercicio.texto, "¿Cuánto suman los ángulos internos de un triángulo?")
        self.assertEqual(ejercicio.tema, self.tema)
        self.assertEqual(ejercicio.dificultad, 'Básico')

    def test_opcion_ejercicio_creation(self):
        """Verifica la creación de opciones para un ejercicio."""
        ejercicio = Ejercicio.objects.create(tema=self.tema, texto="Test", dificultad='Básico')
        opcion = OpcionEjercicio.objects.create(
            ejercicio=ejercicio,
            texto="180 grados",
            es_correcta=True,
            retroalimentacion="Correcto, la suma es 180."
        )
        self.assertEqual(opcion.texto, "180 grados")
        self.assertTrue(opcion.es_correcta)

    def test_resultado_ejercicio_creation(self):
        """Verifica el registro de un resultado de ejercicio."""
        ejercicio = Ejercicio.objects.create(tema=self.tema, texto="Test", dificultad='Básico')
        resultado = ResultadoEjercicio.objects.create(
            usuario=self.user,
            ejercicio=ejercicio,
            es_correcto=True,
            tiempo_empleado=15,
            feedback_mostrado="Buen trabajo."
        )
        self.assertEqual(resultado.usuario, self.user)
        self.assertTrue(resultado.es_correcto)
        self.assertEqual(resultado.tiempo_empleado, 15)
