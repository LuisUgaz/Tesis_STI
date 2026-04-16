from django.test import TestCase
from django.contrib.auth.models import User
from AppTutoria.models import Tema
from AppGestionUsuario.models import Profile
from AppEvaluar.models import ExamenDiagnostico, Pregunta, Opcion, RespuestaUsuario, ResultadoDiagnostico
from AppEvaluar.services import calcular_recomendacion

class AdaptiveInitialLevelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_adaptive', password='password123')
        self.profile = Profile.objects.create(user=self.user, rol='Estudiante')
        self.tema = Tema.objects.create(nombre="Geometría")
        self.examen = ExamenDiagnostico.objects.create(nombre="Test Diagnóstico")
        self.pregunta = Pregunta.objects.create(
            examen=self.examen, texto="Q1", tema=self.tema, tipo='OPCION_MULTIPLE'
        )
        self.op_correcta = Opcion.objects.create(pregunta=self.pregunta, texto="C", es_correcta=True)
        self.op_incorrecta = Opcion.objects.create(pregunta=self.pregunta, texto="I", es_correcta=False)

    def test_assign_basic_level(self):
        """Puntaje 0% -> Nivel Básico."""
        # Registrar fallo
        RespuestaUsuario.objects.create(usuario=self.user, pregunta=self.pregunta, opcion_seleccionada=self.op_incorrecta)
        ResultadoDiagnostico.objects.create(estudiante=self.user, examen=self.examen, puntaje=0)
        
        calcular_recomendacion(self.user)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.nivel_dificultad_actual, 'Básico')

    def test_assign_intermediate_level(self):
        """Puntaje ~50% -> Nivel Intermedio (Simulado con 60% en metrica)."""
        # En la lógica actual, calcular_recomendacion usa las respuestas reales, no solo el puntaje del modelo Resultado.
        # Crearemos 2 preguntas para tener 50%
        p2 = Pregunta.objects.create(examen=self.examen, texto="Q2", tema=self.tema, tipo='OPCION_MULTIPLE')
        oc2 = Opcion.objects.create(pregunta=p2, texto="C", es_correcta=True)
        
        RespuestaUsuario.objects.create(usuario=self.user, pregunta=self.pregunta, opcion_seleccionada=self.op_correcta)
        RespuestaUsuario.objects.create(usuario=self.user, pregunta=p2, opcion_seleccionada=None) # Fallo
        
        ResultadoDiagnostico.objects.create(estudiante=self.user, examen=self.examen, puntaje=50)
        
        calcular_recomendacion(self.user)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.nivel_dificultad_actual, 'Intermedio')

    def test_assign_advanced_level(self):
        """Puntaje 100% -> Nivel Avanzado."""
        RespuestaUsuario.objects.create(usuario=self.user, pregunta=self.pregunta, opcion_seleccionada=self.op_correcta)
        ResultadoDiagnostico.objects.create(estudiante=self.user, examen=self.examen, puntaje=100)
        
        calcular_recomendacion(self.user)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.nivel_dificultad_actual, 'Avanzado')
