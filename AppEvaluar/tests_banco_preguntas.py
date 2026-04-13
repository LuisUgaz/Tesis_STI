from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from AppGestionUsuario.models import Profile
from AppTutoria.models import Tema
from AppEvaluar.models import Ejercicio, OpcionEjercicio

class BancoPreguntasTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.docente_user = User.objects.create_user(username='docente1', password='password123')
        self.docente_profile = Profile.objects.create(user=self.docente_user, rol='Docente')
        
        self.estudiante_user = User.objects.create_user(username='estudiante1', password='password123')
        self.estudiante_profile = Profile.objects.create(user=self.estudiante_user, rol='Estudiante', grado='2do', seccion='A')
        
        self.tema = Tema.objects.create(nombre="Triángulos", slug="triangulos")
        try:
            self.url = reverse('banco_preguntas_create')
        except:
            self.url = '/evaluar/banco-preguntas/nuevo/' # Fallback para la fase roja

    def test_acceso_restringido_a_docentes(self):
        """Solo los docentes deben poder acceder al formulario de creación de preguntas."""
        # Estudiante no debe tener acceso (403 Prohibido)
        self.client.login(username='estudiante1', password='password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
        
        # Docente debe tener acceso (200 OK)
        self.client.login(username='docente1', password='password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_validacion_campos_obligatorios(self):
        """El formulario debe validar que todos los campos requeridos estén presentes."""
        self.client.login(username='docente1', password='password123')
        response = self.client.post(self.url, {}) # Envío vacío
        # En la fase roja, esperamos que falle porque la URL o vista no existen
        # Pero si la vista existiera, validaría los errores del formulario
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertFormError(form, 'texto', 'Este campo es obligatorio.')
        self.assertFormError(form, 'tema', 'Este campo es obligatorio.')
        # self.assertFormError(form, 'dificultad', 'Este campo es obligatorio.') # Dificultad tiene default

    def test_registro_exitoso_pregunta_con_opciones(self):
        """Debe guardar correctamente un ejercicio con sus 5 opciones vinculadas."""
        self.client.login(username='docente1', password='password123')
        
        data = {
            'texto': '¿Cuál es la suma de los ángulos internos de un triángulo?',
            'tema': self.tema.id,
            'dificultad': 'Básico',
            'explicacion_tecnica': 'La suma siempre es 180 grados.',
            # Opciones (InlineFormSet) - Prefijo 'opciones'
            'opciones-TOTAL_FORMS': '5',
            'opciones-INITIAL_FORMS': '0',
            'opciones-MIN_NUM_FORMS': '5',
            'opciones-MAX_NUM_FORMS': '5',
            
            'opciones-0-texto': '180',
            'opciones-0-es_correcta': True,
            'opciones-1-texto': '90',
            'opciones-1-es_correcta': False,
            'opciones-2-texto': '360',
            'opciones-2-es_correcta': False,
            'opciones-3-texto': '270',
            'opciones-3-es_correcta': False,
            'opciones-4-texto': '100',
            'opciones-4-es_correcta': False,
        }
        
        response = self.client.post(self.url, data)
        # Debería redirigir tras éxito
        self.assertEqual(response.status_code, 302)
        
        # Verificar en la base de datos
        ejercicio = Ejercicio.objects.get(texto=data['texto'])
        self.assertEqual(ejercicio.tema, self.tema)
        self.assertEqual(ejercicio.dificultad, 'Básico')
        
        opciones = OpcionEjercicio.objects.filter(ejercicio=ejercicio)
        self.assertEqual(opciones.count(), 5)
        self.assertTrue(opciones.get(texto='180').es_correcta)
        self.assertFalse(opciones.get(texto='90').es_correcta)
