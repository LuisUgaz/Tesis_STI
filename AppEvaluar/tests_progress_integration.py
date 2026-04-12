from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from AppTutoria.models import Tema, ProgresoEstudiante
from AppGestionUsuario.models import Profile
from AppEvaluar.models import Ejercicio, OpcionEjercicio, ExamenDiagnostico, Pregunta, Opcion

class ProgressIntegrationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='student_int', password='password123')
        self.profile = Profile.objects.create(
            user=self.user,
            nombres='Integration',
            apellidos='Student',
            grado='5to',
            seccion='B',
            rol='Estudiante'
        )
        self.tema = Tema.objects.create(nombre='Triángulos')
        self.ejercicio = Ejercicio.objects.create(
            tema=self.tema,
            texto='¿Cuánto es 1+1?',
            dificultad='Básico'
        )
        self.opcion = OpcionEjercicio.objects.create(
            ejercicio=self.ejercicio,
            texto='2',
            es_correcta=True
        )
        self.client = Client()
        self.client.login(username='student_int', password='password123')

    def test_progress_registered_after_exercise(self):
        """Prueba que se registre progreso automáticamente al validar una respuesta de ejercicio."""
        response = self.client.post(reverse('validar_respuesta'), {
            'ejercicio_id': self.ejercicio.id,
            'opcion_id': self.opcion.id,
            'tiempo': 10
        })
        self.assertEqual(response.status_code, 200)
        
        # Verificar que se creó el progreso
        progreso = ProgresoEstudiante.objects.filter(
            usuario=self.user,
            tema=self.tema,
            tipo_actividad='Ejercicio'
        ).first()
        
        self.assertIsNotNone(progreso)
        self.assertEqual(progreso.grado, '5to')
        self.assertEqual(progreso.seccion, 'B')
        self.assertEqual(progreso.referencia_id, self.ejercicio.id)

    def test_progress_registered_after_exam(self):
        """Prueba que se registre progreso automáticamente al finalizar un examen."""
        examen = ExamenDiagnostico.objects.create(nombre='Diagnóstico Inicial', tiempo_limite=30)
        pregunta = Pregunta.objects.create(examen=examen, texto='P1', categoria='Triángulos')
        opcion = Opcion.objects.create(pregunta=pregunta, texto='O1', es_correcta=True)
        
        # Simular envío de examen
        # Primero necesitamos el tema 'Triángulos' ya existe
        
        response = self.client.post(reverse('rendir_examen', args=[examen.id]), {
            f'pregunta_{pregunta.id}': opcion.id
        })
        self.assertEqual(response.status_code, 302) # Redirect to results
        
        # Verificar que se creó el progreso para el tema de la pregunta
        progreso = ProgresoEstudiante.objects.filter(
            usuario=self.user,
            tema=self.tema,
            tipo_actividad='Examen'
        ).first()
        
        self.assertIsNotNone(progreso)
        self.assertEqual(progreso.grado, '5to')
        self.assertEqual(progreso.seccion, 'B')
        self.assertEqual(progreso.referencia_id, examen.id)
