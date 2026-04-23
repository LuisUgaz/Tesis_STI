from django.test import TestCase
from django.contrib.auth.models import User
from .models import Ejercicio, ResultadoEjercicio, RepasoProgramado, ExamenDiagnostico, ResultadoDiagnostico, Pregunta, Opcion, RespuestaUsuario
from AppTutoria.models import Tema
from .services import calcular_recomendacion
from django.utils import timezone
from datetime import timedelta

class SpacedRepetitionIntegrationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='student_integration', password='password123')
        self.tema1 = Tema.objects.create(nombre="Triángulos", slug="triangulos")
        self.tema2 = Tema.objects.create(nombre="Ángulos", slug="angulos")
        
        # Necesitamos un diagnóstico para que el motor funcione normalmente
        diag = ExamenDiagnostico.objects.create(nombre="Test Diag")
        ResultadoDiagnostico.objects.create(estudiante=self.user, examen=diag, puntaje=50)

        # También necesitamos algunas respuestas detalladas para la lógica normal del motor
        pregunta = Pregunta.objects.create(tema=self.tema1, texto="P1", dificultad='Básico')
        opcion = Opcion.objects.create(pregunta=pregunta, texto="O1", es_correcta=True)
        RespuestaUsuario.objects.create(usuario=self.user, pregunta=pregunta, opcion_seleccionada=opcion, tiempo_respuesta=10)

    def test_recommendation_prioritizes_expired_repaso(self):
        """El motor debe recomendar el tema de un repaso vencido sobre cualquier otra debilidad."""
        # 1. Crear un repaso vencido para Tema 2
        RepasoProgramado.objects.create(
            estudiante=self.user,
            tema=self.tema2,
            fecha_proximo_repaso=timezone.now() - timedelta(days=1),
            intervalo=1,
            factor_facilidad=2.5,
            estado=True
        )
        
        # 2. Calcular recomendación
        rec = calcular_recomendacion(self.user)
        
        # Debe ser Tema 2 (repaso) y no Tema 1 u otro basado en el diagnóstico
        self.assertEqual(rec['tema'], self.tema2.nombre)
        self.assertEqual(rec.get('motivo'), 'Repaso programado (Repetición Espaciada)')

    def test_no_repaso_falls_back_to_normal_logic(self):
        """Si no hay repasos vencidos, el motor sigue su lógica normal."""
        # Repaso futuro (no vencido)
        RepasoProgramado.objects.create(
            estudiante=self.user,
            tema=self.tema2,
            fecha_proximo_repaso=timezone.now() + timedelta(days=1),
            intervalo=1,
            factor_facilidad=2.5,
            estado=True
        )
        
        rec = calcular_recomendacion(self.user)
        
        # El motivo no debe ser "Repaso programado"
        self.assertNotEqual(rec.get('motivo'), 'Repaso programado (Repetición Espaciada)')
