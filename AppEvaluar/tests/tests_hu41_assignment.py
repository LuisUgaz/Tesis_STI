from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from AppEvaluar.models import Examen, Pregunta, RecomendacionEstudiante
from AppTutoria.models import Tema
from AppGestionUsuario.models import Profile

class ExamenAssignmentTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.docente = User.objects.create_user(username='docente', password='password123')
        Profile.objects.create(user=self.docente, rol='Docente')
        
        self.estudiante = User.objects.create_user(username='estudiante', password='password123')
        Profile.objects.create(user=self.estudiante, rol='Estudiante', grado='2do', seccion='A')
        
        self.tema = Tema.objects.create(nombre="Ángulos", slug="angulos")
        
        # El estudiante debe tener el tema recomendado para acceder al detalle
        RecomendacionEstudiante.objects.create(usuario=self.estudiante, tema=self.tema.nombre, metrica_desempeno=50)

    def test_docente_puede_asignar_tema_a_examen(self):
        """Verifica que un docente puede asignar un tema a un examen existente."""
        self.client.login(username='docente', password='password123')
        
        # Crear preguntas reales para que asignar_preguntas_aleatorias no falle
        for i in range(2):
            Pregunta.objects.create(texto=f"Q{i}", tema=self.tema)
            
        examen = Examen.objects.create(nombre="Examen de Prueba", cantidad_preguntas=2, tiempo_limite=30, tema=self.tema)
        
        # Cambiar a un nuevo tema
        nuevo_tema = Tema.objects.create(nombre="Triángulos", slug="triangulos")
        # Crear preguntas para el nuevo tema
        for i in range(2):
            Pregunta.objects.create(texto=f"NT{i}", tema=nuevo_tema)
            
        url = reverse('evaluar:examen_update', args=[examen.id])
        
        data = {
            'nombre': 'Examen Modificado',
            'tema': nuevo_tema.id,
            'cantidad_preguntas': 2,
            'tiempo_limite': 30
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302) # Redirección exitosa
        
        examen.refresh_from_db()
        self.assertEqual(examen.tema, nuevo_tema)
        self.assertEqual(examen.nombre, 'Examen Modificado')

    def test_estudiante_ve_examen_en_detalle_tema(self):
        """Verifica que el estudiante ve el examen asignado en la vista de detalle del tema."""
        examen = Examen.objects.create(nombre="Quiz de Ángulos", cantidad_preguntas=1, tiempo_limite=10, tema=self.tema)
        
        self.client.login(username='estudiante', password='password123')
        url = reverse('tutoria:tema_detalle', args=[self.tema.slug])
        
        response = self.client.get(url)
        
        self.assertContains(response, "Quiz de Ángulos")
        self.assertContains(response, f"/evaluar/rendir/{examen.id}/")
