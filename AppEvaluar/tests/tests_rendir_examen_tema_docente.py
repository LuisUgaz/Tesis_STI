from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from AppTutoria.models import Tema
from AppEvaluar.models import Examen, Ejercicio, OpcionEjercicio
from AppGestionUsuario.models import Profile

class RendirExamenTemaDocenteTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Crear docente y estudiante con sus perfiles correspondientes
        self.docente_user = User.objects.create_user(username='docente_test', password='password123')
        Profile.objects.create(user=self.docente_user, rol='Docente', grado='2do', seccion='A')

        self.admin_user = User.objects.create_user(username='admin_sistema', password='password123')
        Profile.objects.create(user=self.admin_user, rol='Administrador', grado='2do', seccion='A')
        
        self.estudiante_user = User.objects.create_user(username='estudiante_test', password='password123')
        Profile.objects.create(user=self.estudiante_user, rol='Estudiante', grado='2do', seccion='A')
        
        # Estructura del tema y examen
        self.tema = Tema.objects.create(nombre="Geometría", slug="geometria")
        self.examen = Examen.objects.create(
            nombre="Examen 1 de Geometría",
            tema=self.tema,
            cantidad_preguntas=1,
            tiempo_limite=15
        )
        
        self.ejercicio = Ejercicio.objects.create(
            texto="¿Cuánto es 2+2 en geometría?",
            tema=self.tema,
            dificultad="Baja",
            es_activo=True
        )
        self.examen.preguntas_ejercicio.add(self.ejercicio)
        
        self.opcion = OpcionEjercicio.objects.create(
            ejercicio=self.ejercicio,
            texto="4",
            es_correcta=True
        )

    def test_docente_puede_ver_examen_sin_restricciones(self):
        """El docente debe ingresar sin validación secuencial ni de intentos."""
        self.client.login(username='docente_test', password='password123')
        url = reverse('evaluar:rendir_examen_tema', args=[self.examen.id])
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "¿Cuánto es 2+2 en geometría?")
        self.assertContains(response, "Volver al Tema")
        self.assertContains(response, "disabled") # Los inputs de selección deben estar deshabilitados

    def test_docente_post_no_registra_respuestas(self):
        """Si un docente intenta hacer POST, debe redirigirse sin registrar nada."""
        self.client.login(username='docente_test', password='password123')
        url = reverse('evaluar:rendir_examen_tema', args=[self.examen.id])
        
        response = self.client.post(url, {
            f'ejercicio_{self.ejercicio.id}': self.opcion.id
        })
        self.assertEqual(response.status_code, 302)
        # Redirige al detalle del tema
        self.assertRedirects(response, reverse('tutoria:tema_detalle', args=[self.tema.slug]))

    def test_administrador_puede_ver_examen_sin_restricciones(self):
        """El administrador debe previsualizar el examen sin registrar respuestas."""
        self.client.login(username='admin_sistema', password='password123')
        url = reverse('evaluar:rendir_examen_tema', args=[self.examen.id])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "disabled")

    def test_estudiante_flujo_normal(self):
        """El estudiante puede ingresar a rendir el examen y se registra su sesión."""
        self.client.login(username='estudiante_test', password='password123')
        url = reverse('evaluar:rendir_examen_tema', args=[self.examen.id])
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Finalizar Evaluación")
        # El timer debe ser visible
        self.assertContains(response, "Tiempo restante:")
