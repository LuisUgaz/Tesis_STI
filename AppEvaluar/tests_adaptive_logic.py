from django.test import TestCase
from django.contrib.auth.models import User
from .models import ExamenDiagnostico, Pregunta, Opcion, RespuestaUsuario, RecomendacionEstudiante, ResultadoDiagnostico
from .services import calcular_recomendacion
from AppTutoria.models import Tema
from AppGestionUsuario.models import Profile

class AdaptiveLogicTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teststudent', password='password123')
        Profile.objects.create(user=self.user, rol='Estudiante', grado='2do', seccion='A')
        
        self.tema1 = Tema.objects.create(nombre="Tema A", slug="tema-a")
        self.tema2 = Tema.objects.create(nombre="Tema B", slug="tema-b")
        
        self.examen = ExamenDiagnostico.objects.create(nombre="Examen Diagnóstico")
        
        # Tema A: 2 preguntas (1 Básica, 1 Avanzada)
        self.p1_a = Pregunta.objects.create(examen=self.examen, texto="P1A", tema=self.tema1, dificultad='Básico')
        self.o1_a = Opcion.objects.create(pregunta=self.p1_a, texto="O1A", es_correcta=True)
        self.p2_a = Pregunta.objects.create(examen=self.examen, texto="P2A", tema=self.tema1, dificultad='Avanzado')
        self.o2_a = Opcion.objects.create(pregunta=self.p2_a, texto="O2A", es_correcta=True)
        
        # Tema B: 2 preguntas (1 Básica, 1 Avanzada)
        self.p1_b = Pregunta.objects.create(examen=self.examen, texto="P1B", tema=self.tema2, dificultad='Básico')
        self.o1_b = Opcion.objects.create(pregunta=self.p1_b, texto="O1B", es_correcta=True)
        self.p2_b = Pregunta.objects.create(examen=self.examen, texto="P2B", tema=self.tema2, dificultad='Avanzado')
        self.o2_b = Opcion.objects.create(pregunta=self.p2_b, texto="O2B", es_correcta=True)

        ResultadoDiagnostico.objects.create(estudiante=self.user, examen=self.examen, puntaje=50)

    def test_weighted_pdp_basic_error_vs_advanced_error(self):
        """
        Escenario: 
        Tema A: Falla la Básica, Acierta la Avanzada.
        Tema B: Acierta la Básica, Falla la Avanzada.
        Ambos tienen 50% de aciertos.
        El PDP de Tema A debería ser MENOR (peor desempeño) que el de Tema B.
        """
        # Respuestas Tema A
        RespuestaUsuario.objects.create(usuario=self.user, pregunta=self.p1_a, opcion_seleccionada=None) # Fallo Básico (Peso 3)
        RespuestaUsuario.objects.create(usuario=self.user, pregunta=self.p2_a, opcion_seleccionada=self.o2_a) # Acierto Avanzado (Peso 1)
        
        # Respuestas Tema B
        RespuestaUsuario.objects.create(usuario=self.user, pregunta=self.p1_b, opcion_seleccionada=self.o1_b) # Acierto Básico (Peso 3)
        RespuestaUsuario.objects.create(usuario=self.user, pregunta=self.p2_b, opcion_seleccionada=None) # Fallo Avanzado (Peso 1)
        
        recomendacion = calcular_recomendacion(self.user)
        
        # El tema recomendado debería ser Tema A (porque el fallo básico penaliza más)
        self.assertEqual(recomendacion['tema'], "Tema A")
        
        # Verificar que el PDP calculado para Tema A sea menor que el de Tema B
        # Tema A: Penalty = 3. Max = 4. PDP = 100 - (3/4 * 100) = 25%
        # Tema B: Penalty = 1. Max = 4. PDP = 100 - (1/4 * 100) = 75%
        self.assertEqual(recomendacion['metrica'], 25.0)

    def test_pdp_penalty_by_excessive_time(self):
        """
        Escenario:
        Estudiante A y B responden correctamente.
        Estudiante A tarda 10s (normal).
        Estudiante B tarda 100s (excesivo).
        El PDP del Estudiante B debería ser menor que 100% debido a la penalización por tiempo.
        """
        # Crear respuestas de otros estudiantes para establecer un promedio (aprox 10s)
        for i in range(5):
            u = User.objects.create_user(username=f'student{i}', password='p')
            RespuestaUsuario.objects.create(usuario=u, pregunta=self.p1_a, opcion_seleccionada=self.o1_a, tiempo_respuesta=10)
        
        # Estudiante bajo prueba (tarda mucho: 100s)
        RespuestaUsuario.objects.create(usuario=self.user, pregunta=self.p1_a, opcion_seleccionada=self.o1_a, tiempo_respuesta=100)
        
        recomendacion = calcular_recomendacion(self.user)
        
        # El puntaje debería ser menor a 100.0 pese a haber acertado la única pregunta
        self.assertLess(recomendacion['metrica'], 100.0)
        self.assertEqual(recomendacion['tema'], "Tema A")

    def test_svm_tie_breaker(self):
        """
        Escenario:
        Tema A y Tema B tienen exactamente el mismo PDP (ambos fallan 1 pregunta básica).
        El orden alfabético elegiría Tema A.
        Configuraremos el contexto para que el SVM elija Tema B.
        """
        # Limpiar respuestas previas
        RespuestaUsuario.objects.all().delete()
        
        # Tema A: 1 fallo básico
        RespuestaUsuario.objects.create(usuario=self.user, pregunta=self.p1_a, opcion_seleccionada=None)
        # Tema B: 1 fallo básico
        RespuestaUsuario.objects.create(usuario=self.user, pregunta=self.p1_b, opcion_seleccionada=None)
        
        # Contexto del estudiante para el SVM
        self.user.profile.puntos_acumulados = 500
        self.user.profile.nivel_estudiante = 5
        self.user.profile.save()
        
        recomendacion = calcular_recomendacion(self.user)
        
        # Si el SVM funciona, debería poder elegir Tema B (según el entrenamiento base que daremos)
        # NOTA: Por ahora el test fallará o elegirá A por orden alfabético si no hay SVM.
        self.assertEqual(recomendacion['tema'], "Tema B")

    def test_svm_fallback_to_alphabetical(self):
        """
        Escenario:
        Tema A y Tema B empatados.
        Estudiante con perfil inicial (Case B/D del training).
        El SVM debería predecir 0, lo que resulta en el primer tema (alfabético): Tema A.
        """
        RespuestaUsuario.objects.all().delete()
        RespuestaUsuario.objects.create(usuario=self.user, pregunta=self.p1_a, opcion_seleccionada=None)
        RespuestaUsuario.objects.create(usuario=self.user, pregunta=self.p1_b, opcion_seleccionada=None)
        
        # Perfil inicial
        self.user.profile.puntos_acumulados = 0
        self.user.profile.nivel_estudiante = 1
        self.user.profile.save()
        
        recomendacion = calcular_recomendacion(self.user)
        
        # Debe caer en Tema A (orden alfabético por predicción 0)
        self.assertEqual(recomendacion['tema'], "Tema A")

    def test_difficulty_adjustment_diagnostic(self):
        """
        Verifica que el nivel del perfil cambie según el PDP del diagnóstico.
        Regla: PDP <= 40 -> Básico.
        """
        # Limpiar respuestas
        RespuestaUsuario.objects.all().delete()
        
        # Tema A: Fallo crítico (Básico) -> PDP = 0
        RespuestaUsuario.objects.create(usuario=self.user, pregunta=self.p1_a, opcion_seleccionada=None)
        
        # Iniciar con nivel Avanzado para ver si baja
        self.user.profile.nivel_dificultad_actual = 'Avanzado'
        self.user.profile.save()
        
        calcular_recomendacion(self.user)
        
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.nivel_dificultad_actual, 'Básico')

    def test_svm_dynamic_learning(self):
        """
        Verifica que el SVM se registre en LogEntrenamientoSVM y use datos reales si existen.
        """
        from .models import LogEntrenamientoSVM
        
        # Escenario de empate
        RespuestaUsuario.objects.all().delete()
        RespuestaUsuario.objects.create(usuario=self.user, pregunta=self.p1_a, opcion_seleccionada=None)
        RespuestaUsuario.objects.create(usuario=self.user, pregunta=self.p1_b, opcion_seleccionada=None)
        
        # Ejecutar recomendación
        calcular_recomendacion(self.user)
        
        # Verificar que se creó un log pendiente
        log = LogEntrenamientoSVM.objects.filter(estudiante=self.user).last()
        self.assertIsNotNone(log)
        self.assertIsNone(log.fue_exito)
        
        # Simular éxito de la recomendación (estudiante acierta un ejercicio del tema elegido)
        from .services import evaluar_exito_recomendacion
        evaluar_exito_recomendacion(self.user, log.tema_elegido.nombre, es_correcto=True)
        
        log.refresh_from_db()
        self.assertTrue(log.fue_exito)
        
        # Ahora creamos 10 logs de éxito para forzar el entrenamiento dinámico
        for i in range(10):
            LogEntrenamientoSVM.objects.create(
                estudiante=self.user,
                tema_elegido=self.tema2,
                tiempo_promedio=10.0,
                nivel_estudiante=3,
                puntos_acumulados=1000.0,
                fue_exito=True
            )
        
        # Volver a calcular recomendación (debería usar entrenamiento dinámico)
        # Esto valida que el código no explote al usar StandardScaler y SVC con datos de la DB
        recomendacion = calcular_recomendacion(self.user)
        self.assertIn(recomendacion['tema'], ["Tema A", "Tema B"])




