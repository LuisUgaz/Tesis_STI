from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from AppGestionUsuario.models import Profile
from AppTutoria.models import Tema
from AppEvaluar.models import RecomendacionEstudiante, Ejercicio, OpcionEjercicio, ResultadoEjercicio
import time

class EjercicioIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='alumno_final', password='password123')
        self.profile = Profile.objects.create(user=self.user, rol='Estudiante')
        self.tema = Tema.objects.create(nombre="Triángulos", slug="triangulos")
        
        # Crear datos de prueba
        self.ejercicio = Ejercicio.objects.create(tema=self.tema, texto="¿Suma?", dificultad='Básico')
        self.opcion = OpcionEjercicio.objects.create(
            ejercicio=self.ejercicio, texto="180", es_correcta=True, retroalimentacion="OK"
        )
        
        # Asignar recomendación
        RecomendacionEstudiante.objects.create(usuario=self.user, tema=self.tema.nombre, metrica_desempeno=40)

    def test_flujo_completo_practica(self):
        """Verifica el flujo desde inicio hasta guardado de resultado."""
        self.client.login(username='alumno_final', password='password123')
        
        # 1. Acceder a la vista de inicio
        response = self.client.get(reverse('iniciar_practica'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "¿Suma?")
        
        # 2. Enviar respuesta correcta (simulando Fetch)
        response_ajax = self.client.post(reverse('validar_respuesta'), {
            'ejercicio_id': self.ejercicio.id,
            'opcion_id': self.opcion.id,
            'tiempo': 5
        })
        self.assertEqual(response_ajax.status_code, 200)
        self.assertTrue(response_ajax.json()['es_correcto'])
        
        # 3. Verificar que se creó el registro de resultado
        resultado = ResultadoEjercicio.objects.get(usuario=self.user, ejercicio=self.ejercicio)
        self.assertTrue(resultado.es_correcto)
        self.assertEqual(resultado.tiempo_empleado, 5)
        self.assertEqual(resultado.feedback_mostrado, "OK")
