from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from AppGestionUsuario.models import Profile
from AppTutoria.models import Tema, ProgresoEstudiante
from .models import ExamenDiagnostico, ResultadoDiagnostico, Ejercicio, ResultadoEjercicio

class HistorialResultadosTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='student1', password='password123')
        Profile.objects.create(user=self.user1, nombres='Juan', apellidos='Perez', rol='Estudiante')
        
        self.user2 = User.objects.create_user(username='student2', password='password123')
        Profile.objects.create(user=self.user2, nombres='Maria', apellidos='Gomez', rol='Estudiante')

        self.tema_triangulos = Tema.objects.create(nombre="Triángulos", slug="triangulos")
        self.tema_angulos = Tema.objects.create(nombre="Ángulos", slug="angulos")

        # Datos para user1
        self.progreso1 = ProgresoEstudiante.objects.create(
            usuario=self.user1,
            tema=self.tema_triangulos,
            tipo_actividad='Ejercicio',
            grado='2',
            seccion='A'
        )
        
        # Datos para user2
        self.progreso2 = ProgresoEstudiante.objects.create(
            usuario=self.user2,
            tema=self.tema_angulos,
            tipo_actividad='Video',
            grado='2',
            seccion='B'
        )

        self.url_historial = reverse('historial_resultados')

    def test_historial_requires_login(self):
        response = self.client.get(self.url_historial)
        self.assertEqual(response.status_code, 302) # Redirect to login

    def test_historial_only_shows_own_data(self):
        self.client.login(username='student1', password='password123')
        response = self.client.get(self.url_historial)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Triángulos")
        # El tema Ángulos pertenece a student2, no debe estar en los resultados
        # pero sí puede estar en el selector de filtros si todos los temas se cargan.
        # Verificamos que no esté en el cuerpo de la tabla (progresos)
        progresos = response.context['progresos']
        for p in progresos:
            self.assertNotEqual(p.tema.nombre, "Ángulos")

    def test_historial_filter_by_tema(self):
        # Crear otro progreso para user1 con diferente tema
        ProgresoEstudiante.objects.create(
            usuario=self.user1,
            tema=self.tema_angulos,
            tipo_actividad='Teoría',
            grado='2',
            seccion='A'
        )
        self.client.login(username='student1', password='password123')
        
        # Filtrar por Triángulos
        response = self.client.get(self.url_historial, {'tema': self.tema_triangulos.id})
        self.assertContains(response, "Triángulos")
        self.assertNotContains(response, "Teoría") # El de Ángulos es Teoría

    def test_historial_order_chronological(self):
        import time
        # El primero ya fue creado en setUp (Triángulos)
        time.sleep(0.1)
        # Crear uno nuevo (Ángulos)
        ProgresoEstudiante.objects.create(
            usuario=self.user1,
            tema=self.tema_angulos,
            tipo_actividad='Video',
            grado='2',
            seccion='A'
        )
        self.client.login(username='student1', password='password123')
        
        # Por defecto descendente (más reciente primero)
        response = self.client.get(self.url_historial)
        items = list(response.context['progresos'])
        self.assertEqual(items[0].tema.nombre, "Ángulos")
        self.assertEqual(items[1].tema.nombre, "Triángulos")

        # Orden ascendente
        response = self.client.get(self.url_historial, {'order': 'asc'})
        items = list(response.context['progresos'])
        self.assertEqual(items[0].tema.nombre, "Triángulos")
        self.assertEqual(items[1].tema.nombre, "Ángulos")

    def test_historial_shows_detailed_results(self):
        # 1. Ejercicio Correcto
        ejercicio = Ejercicio.objects.create(tema=self.tema_triangulos, texto="Ej 1", dificultad='Básico')
        ResultadoEjercicio.objects.create(
            usuario=self.user1,
            ejercicio=ejercicio,
            es_correcto=True,
            tiempo_empleado=10,
            feedback_mostrado="Bien"
        )
        ProgresoEstudiante.objects.create(
            usuario=self.user1,
            tema=self.tema_triangulos,
            tipo_actividad='Ejercicio',
            grado='2',
            seccion='A',
            referencia_id=ejercicio.id
        )

        # 2. Examen con Puntaje
        examen = ExamenDiagnostico.objects.create(nombre="Examen Final")
        ResultadoDiagnostico.objects.create(
            estudiante=self.user1,
            examen=examen,
            puntaje=85.0
        )
        ProgresoEstudiante.objects.create(
            usuario=self.user1,
            tema=self.tema_triangulos,
            tipo_actividad='Examen',
            grado='2',
            seccion='A',
            referencia_id=examen.id
        )

        self.client.login(username='student1', password='password123')
        response = self.client.get(self.url_historial)
        
        self.assertContains(response, "Correcto")
        self.assertContains(response, "Puntaje: 85")
