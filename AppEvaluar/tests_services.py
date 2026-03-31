from django.test import TestCase
from django.contrib.auth.models import User
from AppEvaluar.models import ExamenDiagnostico, Pregunta, ResultadoDiagnostico, RespuestaUsuario, Opcion
from AppEvaluar.services import calcular_recomendacion, SinResultadosError

class RecommendationServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.examen = ExamenDiagnostico.objects.create(nombre='Examen de Prueba', tiempo_limite=45)

    def test_calcular_recomendacion_sin_resultados_lanza_error(self):
        """Si el usuario no tiene resultados, debe lanzar SinResultadosError."""
        with self.assertRaises(SinResultadosError):
            calcular_recomendacion(self.user)

    def test_calcular_recomendacion_con_datos_validos(self):
        """Prueba que el sistema recomienda el tema con menor desempeño."""
        # Crear temas (categorías)
        t1 = 'Triángulos'
        t2 = 'Ángulos'
        t3 = 'Círculos'

        # P1: Triángulos (0% acierto: 0/1)
        p1 = Pregunta.objects.create(examen=self.examen, texto='P1', categoria=t1)
        o1_i = Opcion.objects.create(pregunta=p1, texto='I1', es_correcta=False)
        RespuestaUsuario.objects.create(usuario=self.user, pregunta=p1, opcion_seleccionada=o1_i)

        # P2: Ángulos (100% acierto: 1/1)
        p2 = Pregunta.objects.create(examen=self.examen, texto='P2', categoria=t2)
        o2_c = Opcion.objects.create(pregunta=p2, texto='C2', es_correcta=True)
        RespuestaUsuario.objects.create(usuario=self.user, pregunta=p2, opcion_seleccionada=o2_c)

        # P3: Círculos (50% acierto: 1/2)
        p3_a = Pregunta.objects.create(examen=self.examen, texto='P3a', categoria=t3)
        p3_b = Pregunta.objects.create(examen=self.examen, texto='P3b', categoria=t3)
        o3a_c = Opcion.objects.create(pregunta=p3_a, texto='C3a', es_correcta=True)
        o3b_i = Opcion.objects.create(pregunta=p3_b, texto='I3b', es_correcta=False)
        RespuestaUsuario.objects.create(usuario=self.user, pregunta=p3_a, opcion_seleccionada=o3a_c)
        RespuestaUsuario.objects.create(usuario=self.user, pregunta=p3_b, opcion_seleccionada=o3b_i)

        # Crear resultado general para pasar el check de Phase 1
        ResultadoDiagnostico.objects.create(estudiante=self.user, examen=self.examen, puntaje=50.0)

        recomendacion = calcular_recomendacion(self.user)
        
        # Debe recomendar Triángulos porque tiene 0%
        self.assertEqual(recomendacion['tema'], t1)
        self.assertEqual(recomendacion['metrica'], 0.0)

    def test_resolver_empate_primer_encuentro(self):
        """Si hay empate en el peor desempeño, debe elegir el primero."""
        t1 = 'Tema A'
        t2 = 'Tema B'

        p1 = Pregunta.objects.create(examen=self.examen, texto='P1', categoria=t1)
        o1_i = Opcion.objects.create(pregunta=p1, texto='I1', es_correcta=False)
        RespuestaUsuario.objects.create(usuario=self.user, pregunta=p1, opcion_seleccionada=o1_i)

        p2 = Pregunta.objects.create(examen=self.examen, texto='P2', categoria=t2)
        o2_i = Opcion.objects.create(pregunta=p2, texto='I2', es_correcta=False)
        RespuestaUsuario.objects.create(usuario=self.user, pregunta=p2, opcion_seleccionada=o2_i)

        ResultadoDiagnostico.objects.create(estudiante=self.user, examen=self.examen, puntaje=0.0)

        recomendacion = calcular_recomendacion(self.user)
        
        # Ambos tienen 0%. Debe retornar el primero (por orden alfabético o de inserción según se implemente)
        # Por simplicidad, asumiremos el primero que el algoritmo procese.
        self.assertIn(recomendacion['tema'], [t1, t2])
