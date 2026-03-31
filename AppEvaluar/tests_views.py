from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from AppGestionUsuario.models import Profile
from .models import ExamenDiagnostico, Pregunta, Opcion, RespuestaUsuario

class EvaluarViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_student = User.objects.create_user(username='student', password='password123')
        Profile.objects.create(user=self.user_student, nombres='Juan', apellidos='Perez', rol='Estudiante')
        
        self.user_teacher = User.objects.create_user(username='teacher', password='password123')
        Profile.objects.create(user=self.user_teacher, nombres='Maria', apellidos='Gomez', rol='Docente')

        self.examen = ExamenDiagnostico.objects.create(nombre="Examen Test", tiempo_limite=30)
        self.pregunta = Pregunta.objects.create(examen=self.examen, texto="Pregunta 1", tipo='OPCION_MULTIPLE', categoria='Gral')
        Opcion.objects.create(pregunta=self.pregunta, texto="Opcion A", es_correcta=True)

        self.url_examen = reverse('rendir_examen', kwargs={'examen_id': self.examen.id})

    def test_examen_view_requires_login(self):
        response = self.client.get(self.url_examen)
        self.assertEqual(response.status_code, 302) # Redirect to login

    def test_examen_view_restricted_to_students(self):
        self.client.login(username='teacher', password='password123')
        response = self.client.get(self.url_examen)
        self.assertEqual(response.status_code, 403) # Forbidden

    def test_examen_view_accessible_to_students(self):
        self.client.login(username='student', password='password123')
        response = self.client.get(self.url_examen)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AppEvaluar/rendir_examen.html')
        self.assertContains(response, "Pregunta 1")

    def test_examen_submission_saves_responses(self):
        self.client.login(username='student', password='password123')
        data = {
            f'pregunta_{self.pregunta.id}': Opcion.objects.get(texto="Opcion A").id
        }
        response = self.client.post(self.url_examen, data)
        # Por ahora debe redirigir a algún lugar (ej. home o resultados)
        self.assertEqual(RespuestaUsuario.objects.count(), 1)
        respuesta = RespuestaUsuario.objects.first()
        self.assertEqual(respuesta.opcion_seleccionada.texto, "Opcion A")
        self.assertEqual(respuesta.usuario, self.user_student)

    def test_results_view_shows_score(self):
        self.client.login(username='student', password='password123')
        # Crear una respuesta previa
        RespuestaUsuario.objects.create(
            usuario=self.user_student,
            pregunta=self.pregunta,
            opcion_seleccionada=Opcion.objects.get(texto="Opcion A")
        )
        url_resultados = reverse('ver_resultados', kwargs={'examen_id': self.examen.id})
        response = self.client.get(url_resultados)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AppEvaluar/resultados.html')
        self.assertContains(response, "20.0") # Puntaje total (1 de 1 correcta = 20)
        self.assertContains(response, "Gral") # Tema
