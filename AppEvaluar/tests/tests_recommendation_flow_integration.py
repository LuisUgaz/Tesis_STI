from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from AppTutoria.models import Tema
from AppEvaluar.models import ExamenDiagnostico, Pregunta, Opcion, ResultadoDiagnostico, RecomendacionEstudiante, RespuestaUsuario
from AppGestionUsuario.models import Profile
from unittest.mock import patch, MagicMock

class RecommendationFlowIntegrationTest(TestCase):
    def setUp(self):
        # 1. Crear Temas
        self.tema_angulos = Tema.objects.create(nombre="Ángulos", slug="angulos")
        self.tema_triangulos = Tema.objects.create(nombre="Triángulos", slug="triangulos")
        
        # 2. Crear Usuario Estudiante
        self.user = User.objects.create_user(username='estudiante_test_new', password='password123')
        self.profile = Profile.objects.create(user=self.user, rol='Estudiante', grado='2do', seccion='A')
        
        # 3. Crear Examen Diagnóstico
        self.examen = ExamenDiagnostico.objects.create(nombre="Examen Inicial", tiempo_limite=45)
        
        # 4. Crear Preguntas
        # Tema Ángulos: 2 preguntas básicas
        self.p_ang1 = Pregunta.objects.create(examen=self.examen, texto="¿P1 Angulos?", tema=self.tema_angulos, dificultad='Básico', tipo='OPCION_MULTIPLE')
        self.o_ang1_c = Opcion.objects.create(pregunta=self.p_ang1, texto="Correcta", es_correcta=True)
        self.o_ang1_i = Opcion.objects.create(pregunta=self.p_ang1, texto="Incorrecta", es_correcta=False)
        
        self.p_ang2 = Pregunta.objects.create(examen=self.examen, texto="¿P2 Angulos?", tema=self.tema_angulos, dificultad='Básico', tipo='OPCION_MULTIPLE')
        self.o_ang2_c = Opcion.objects.create(pregunta=self.p_ang2, texto="Correcta", es_correcta=True)
        
        # Tema Triángulos: 2 preguntas básicas
        self.p_tri1 = Pregunta.objects.create(examen=self.examen, texto="¿P1 Triangulos?", tema=self.tema_triangulos, dificultad='Básico', tipo='OPCION_MULTIPLE')
        self.o_tri1_c = Opcion.objects.create(pregunta=self.p_tri1, texto="Correcta", es_correcta=True)
        self.o_tri1_i = Opcion.objects.create(pregunta=self.p_tri1, texto="Incorrecta", es_correcta=False)
        
        self.p_tri2 = Pregunta.objects.create(examen=self.examen, texto="¿P2 Triangulos?", tema=self.tema_triangulos, dificultad='Básico', tipo='OPCION_MULTIPLE')
        self.o_tri2_c = Opcion.objects.create(pregunta=self.p_tri2, texto="Correcta", es_correcta=True)

        self.client = Client()

    def test_full_diagnostic_to_recommendation_flow(self):
        """
        Prueba el flujo completo:
        1. Login.
        2. Realizar examen (fallando en Triángulos deliberadamente).
        3. Verificar creación de Resultado y Recomendación.
        4. Verificar redirección a lista de temas con prioridad.
        5. Verificar acceso restringido a otros temas.
        """
        # 1. Login
        login_success = self.client.login(username='estudiante_test_new', password='password123')
        self.assertTrue(login_success)

        # 2. Realizar examen
        # Tema Ángulos: Todas correctas (2/2)
        # Tema Triángulos: Todas incorrectas (0/2) -> Debería recomendar Triángulos
        data = {
            f'pregunta_{self.p_ang1.id}': self.o_ang1_c.id,
            f'tiempo_pregunta_{self.p_ang1.id}': '10',
            f'pregunta_{self.p_ang2.id}': self.o_ang2_c.id,
            f'tiempo_pregunta_{self.p_ang2.id}': '10',
            f'pregunta_{self.p_tri1.id}': self.o_tri1_i.id,
            f'tiempo_pregunta_{self.p_tri1.id}': '10',
            f'pregunta_{self.p_tri2.id}': '', # Dejada en blanco
            f'tiempo_pregunta_{self.p_tri2.id}': '10',
        }
        
        response = self.client.post(reverse('evaluar:rendir_examen', args=[self.examen.id]), data)
        
        # Debe redirigir a resultados
        self.assertRedirects(response, reverse('evaluar:ver_resultados', args=[self.examen.id]))

        # 3. Verificar Persistencia
        resultado = ResultadoDiagnostico.objects.get(estudiante=self.user, examen=self.examen)
        self.assertEqual(resultado.puntaje, 50.0) # 2 de 4 correctas

        recomendacion = RecomendacionEstudiante.objects.get(usuario=self.user)
        self.assertEqual(recomendacion.tema, "Triángulos")

        # 4. Verificar Redirección a lista de temas y prioridad
        response = self.client.get(reverse('tutoria:lista_temas'))
        self.assertEqual(response.status_code, 200)
        # El primer tema en el contexto debe ser el recomendado (Triángulos)
        temas_en_contexto = response.context['temas']
        self.assertEqual(temas_en_contexto[0].nombre, "Triángulos")

        # 5. Verificar Acceso Restringido
        # Acceso al tema recomendado (Triángulos) -> Permitido
        response = self.client.get(reverse('tutoria:tema_detalle', args=[self.tema_triangulos.slug]))
        self.assertEqual(response.status_code, 200)

        # Acceso al tema NO recomendado (Ángulos) -> Redirigido
        response = self.client.get(reverse('tutoria:tema_detalle', args=[self.tema_angulos.slug]))
        self.assertRedirects(response, reverse('tutoria:lista_temas'))

    @patch('google.generativeai.GenerativeModel.generate_content')
    def test_ia_feedback_integration(self, mock_generate):
        """
        Verifica que el endpoint de IA feedback funcione correctamente.
        """
        self.client.login(username='estudiante_test_new', password='password123')
        
        # Crear una respuesta para probar
        respuesta = RespuestaUsuario.objects.create(
            usuario=self.user,
            pregunta=self.p_tri1,
            opcion_seleccionada=self.o_tri1_i,
            tiempo_respuesta=10
        )

        # Mock de la IA
        mock_response = MagicMock()
        mock_response.text = "Explicación de la IA: Fallaste porque los triángulos tienen 3 lados."
        mock_generate.return_value = mock_response

        # Llamar al endpoint AJAX
        response = self.client.get(reverse('evaluar:ia_feedback', args=[respuesta.id]))
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['feedback'], mock_response.text)
        self.assertTrue(mock_generate.called)

    def test_unauthorized_ia_feedback(self):
        """Verifica que un usuario no pueda pedir feedback de respuestas de otros."""
        otro_usuario = User.objects.create_user(username='otro', password='password')
        respuesta_otro = RespuestaUsuario.objects.create(
            usuario=otro_usuario,
            pregunta=self.p_tri1,
            opcion_seleccionada=self.o_tri1_i
        )

        self.client.login(username='estudiante_test_new', password='password123')
        response = self.client.get(reverse('evaluar:ia_feedback', args=[respuesta_otro.id]))
        
        self.assertEqual(response.status_code, 403)

    def test_recommendation_persistence_on_visit(self):
        """
        Verifica que la recomendación persista y afecte la UI en visitas posteriores
        sin necesidad de rendir el examen nuevamente.
        """
        # 1. Crear recomendación previa
        RecomendacionEstudiante.objects.create(
            usuario=self.user,
            tema="Ángulos",
            metrica_desempeno=30.0
        )
        
        self.client.login(username='estudiante_test_new', password='password123')
        
        # 2. Visitar lista de temas
        response = self.client.get(reverse('tutoria:lista_temas'))
        
        # 3. Verificar prioridad
        temas = response.context['temas']
        self.assertEqual(temas[0].nombre, "Ángulos")
        
        # 4. Verificar acceso
        response = self.client.get(reverse('tutoria:tema_detalle', args=[self.tema_angulos.slug]))
        self.assertEqual(response.status_code, 200)
