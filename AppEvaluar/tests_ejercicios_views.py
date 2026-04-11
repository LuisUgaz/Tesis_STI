from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from AppGestionUsuario.models import Profile
from AppTutoria.models import Tema
from AppEvaluar.models import RecomendacionEstudiante, Ejercicio, OpcionEjercicio, ResultadoEjercicio

class EjercicioViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='estudiante1', password='password123')
        self.profile = Profile.objects.create(user=self.user, rol='Estudiante')
        self.tema = Tema.objects.create(nombre="Triángulos", slug="triangulos")
        
        # Crear ejercicios
        self.ejercicio = Ejercicio.objects.create(tema=self.tema, texto="¿Suma?", dificultad='Básico')
        self.opcion_correcta = OpcionEjercicio.objects.create(
            ejercicio=self.ejercicio, texto="180", es_correcta=True, retroalimentacion="¡Bien!"
        )
        self.opcion_incorrecta = OpcionEjercicio.objects.create(
            ejercicio=self.ejercicio, texto="90", es_correcta=False, retroalimentacion="Mal."
        )

    def test_iniciar_practica_sin_recomendacion(self):
        """No debería poder iniciar práctica si no tiene tema recomendado."""
        self.client.login(username='estudiante1', password='password123')
        response = self.client.get(reverse('iniciar_practica'))
        self.assertEqual(response.status_code, 403)

    def test_iniciar_practica_con_recomendacion(self):
        """Debería mostrar la página de práctica con los ejercicios del tema."""
        RecomendacionEstudiante.objects.create(usuario=self.user, tema=self.tema.nombre, metrica_desempeno=50)
        self.client.login(username='estudiante1', password='password123')
        response = self.client.get(reverse('iniciar_practica'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AppEvaluar/practica_ejercicio.html')

    def test_validar_respuesta_correcta(self):
        """Debería registrar el resultado como correcto y devolver feedback."""
        RecomendacionEstudiante.objects.create(usuario=self.user, tema=self.tema.nombre, metrica_desempeno=50)
        self.client.login(username='estudiante1', password='password123')
        
        response = self.client.post(reverse('validar_respuesta'), {
            'ejercicio_id': self.ejercicio.id,
            'opcion_id': self.opcion_correcta.id,
            'tiempo': 10
        })
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['es_correcto'])
        self.assertEqual(data['feedback'], "¡Bien!")
        
        # Verificar persistencia
        resultado = ResultadoEjercicio.objects.get(usuario=self.user, ejercicio=self.ejercicio)
        self.assertTrue(resultado.es_correcto)
        self.assertEqual(resultado.tiempo_empleado, 10)

    def test_validar_respuesta_feedback_mixto(self):
        """Debería devolver tanto el feedback de la opción como la explicación técnica del ejercicio."""
        # 1. Configurar ejercicio con explicación técnica
        self.ejercicio.explicacion_tecnica = "La suma interna de ángulos es 180."
        self.ejercicio.save()
        
        RecomendacionEstudiante.objects.create(usuario=self.user, tema=self.tema.nombre, metrica_desempeno=50)
        self.client.login(username='estudiante1', password='password123')
        
        # 2. Enviar respuesta incorrecta
        response = self.client.post(reverse('validar_respuesta'), {
            'ejercicio_id': self.ejercicio.id,
            'opcion_id': self.opcion_incorrecta.id,
            'tiempo': 5
        })
        
        # 3. Validar respuesta JSON
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['feedback'], "Mal.")
        self.assertEqual(data['explicacion_tecnica'], "La suma interna de ángulos es 180.")
        
        # 4. Verificar persistencia (concatenación)
        resultado = ResultadoEjercicio.objects.get(usuario=self.user, ejercicio=self.ejercicio)
        self.assertIn("Mal.", resultado.feedback_mostrado)
        self.assertIn("La suma interna de ángulos es 180.", resultado.feedback_mostrado)
