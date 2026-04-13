from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from AppGestionUsuario.models import Profile
from AppTutoria.models import Tema
from AppEvaluar.models import Ejercicio

class BancoPreguntasFilterTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.docente_user = User.objects.create_user(username='docente_filter', password='password123')
        self.docente_profile = Profile.objects.create(user=self.docente_user, rol='Docente')
        
        self.tema1 = Tema.objects.create(nombre="Triángulos", slug="triangulos")
        self.tema2 = Tema.objects.create(nombre="Ángulos", slug="angulos")
        
        # Crear datos de prueba
        Ejercicio.objects.create(tema=self.tema1, texto="Pregunta T1-B", dificultad="Básico")
        Ejercicio.objects.create(tema=self.tema1, texto="Pregunta T1-I", dificultad="Intermedio")
        Ejercicio.objects.create(tema=self.tema2, texto="Pregunta T2-B", dificultad="Básico")
        
        self.url_list = reverse('banco_preguntas_list')
        self.client.login(username='docente_filter', password='password123')

    def test_filtrar_por_tema(self):
        """Verifica que el listado se filtre correctamente por el tema seleccionado."""
        response = self.client.get(self.url_list, {'tema': self.tema1.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pregunta T1-B")
        self.assertContains(response, "Pregunta T1-I")
        self.assertNotContains(response, "Pregunta T2-B")

    def test_filtrar_por_dificultad(self):
        """Verifica que el listado se filtre correctamente por la dificultad seleccionada."""
        response = self.client.get(self.url_list, {'dificultad': 'Básico'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pregunta T1-B")
        self.assertContains(response, "Pregunta T2-B")
        self.assertNotContains(response, "Pregunta T1-I")

    def test_filtrar_por_tema_y_dificultad(self):
        """Verifica el filtrado combinado por ambos criterios."""
        response = self.client.get(self.url_list, {'tema': self.tema1.id, 'dificultad': 'Intermedio'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pregunta T1-I")
        self.assertNotContains(response, "Pregunta T1-B")
        self.assertNotContains(response, "Pregunta T2-B")
