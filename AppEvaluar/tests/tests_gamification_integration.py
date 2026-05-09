from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from AppGestionUsuario.models import Profile
from AppTutoria.models import Tema
from AppEvaluar.models import Ejercicio, OpcionEjercicio, RecomendacionEstudiante

class GamificationIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='gamestudent', password='password123')
        self.profile = Profile.objects.create(
            user=self.user, 
            nombres='Game', 
            apellidos='Student', 
            rol='Estudiante',
            nivel_dificultad_actual='Básico',
            grado='5to',
            seccion='A'
        )
        self.tema = Tema.objects.create(nombre="Triángulos", slug="triangulos")
        self.ejercicio_basico = Ejercicio.objects.create(tema=self.tema, texto="¿Suma?", dificultad='Básico')
        self.opcion_correcta = OpcionEjercicio.objects.create(
            ejercicio=self.ejercicio_basico, texto="180", es_correcta=True
        )
        self.opcion_incorrecta = OpcionEjercicio.objects.create(
            ejercicio=self.ejercicio_basico, texto="90", es_correcta=False
        )
        
        # Necesario para iniciar práctica
        RecomendacionEstudiante.objects.create(usuario=self.user, tema=self.tema.nombre, metrica_desempeno=50)

    def test_points_assigned_on_correct_answer_basic(self):
        """Al responder correctamente un ejercicio básico, el perfil debe ganar 10 puntos."""
        self.client.login(username='gamestudent', password='password123')
        
        self.client.post(reverse('evaluar:validar_respuesta'), {
            'ejercicio_id': self.ejercicio_basico.id,
            'opcion_id': self.opcion_correcta.id,
            'tiempo': 10
        })
        
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.puntos_acumulados, 10)

    def test_points_assigned_on_incorrect_answer(self):
        """Al responder incorrectamente, el perfil debe ganar 2 puntos (esfuerzo)."""
        self.client.login(username='gamestudent', password='password123')
        
        self.client.post(reverse('evaluar:validar_respuesta'), {
            'ejercicio_id': self.ejercicio_basico.id,
            'opcion_id': self.opcion_incorrecta.id,
            'tiempo': 10
        })
        
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.puntos_acumulados, 2)

    def test_points_response_json(self):
        """La respuesta JSON de validación debe incluir los puntos ganados (para el frontend)."""
        self.client.login(username='gamestudent', password='password123')
        
        response = self.client.post(reverse('evaluar:validar_respuesta'), {
            'ejercicio_id': self.ejercicio_basico.id,
            'opcion_id': self.opcion_correcta.id,
            'tiempo': 10
        })
        
        data = response.json()
        self.assertIn('puntos_ganados', data)
        self.assertEqual(data['puntos_ganados'], 10)
        self.assertEqual(data['total_puntos'], 10)
