from django.test import TestCase
from django.contrib.auth.models import User
from AppGestionUsuario.models import Profile
from AppTutoria.models import Tema
from AppEvaluar.models import Ejercicio, ResultadoEjercicio
from AppEvaluar.services import ajustar_dificultad_estudiante

class AdaptiveAdjustmentTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='adapter', password='password123')
        self.profile = Profile.objects.create(user=self.user, rol='Estudiante', nivel_dificultad_actual='Básico')
        self.tema = Tema.objects.create(nombre="Triángulos", slug="triangulos")
        
        # Crear 5 ejercicios para la sesión
        self.ejercicios = []
        for i in range(5):
            self.ejercicios.append(Ejercicio.objects.create(tema=self.tema, texto=f"E{i}", dificultad='Básico'))

    def test_level_up_on_80_percent(self):
        """Si acierta 4 de 5 (80%), sube a Intermedio."""
        for i in range(4):
            ResultadoEjercicio.objects.create(
                usuario=self.user, ejercicio=self.ejercicios[i], es_correcto=True, tiempo_empleado=10, feedback_mostrado="OK"
            )
        # El 5to es incorrecto
        ResultadoEjercicio.objects.create(
            usuario=self.user, ejercicio=self.ejercicios[4], es_correcto=False, tiempo_empleado=10, feedback_mostrado="FAIL"
        )
        
        ajustar_dificultad_estudiante(self.user)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.nivel_dificultad_actual, 'Intermedio')

    def test_stay_on_low_performance(self):
        """Si acierta 2 de 5 (40%), se mantiene en Básico."""
        for i in range(2):
            ResultadoEjercicio.objects.create(
                usuario=self.user, ejercicio=self.ejercicios[i], es_correcto=True, tiempo_empleado=10, feedback_mostrado="OK"
            )
        for i in range(2, 5):
            ResultadoEjercicio.objects.create(
                usuario=self.user, ejercicio=self.ejercicios[i], es_correcto=False, tiempo_empleado=10, feedback_mostrado="FAIL"
            )
        
        ajustar_dificultad_estudiante(self.user)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.nivel_dificultad_actual, 'Básico')

    def test_max_level_reached(self):
        """Si ya está en Avanzado, no sube más."""
        self.profile.nivel_dificultad_actual = 'Avanzado'
        self.profile.save()
        
        for i in range(5):
            ResultadoEjercicio.objects.create(
                usuario=self.user, ejercicio=self.ejercicios[i], es_correcto=True, tiempo_empleado=10, feedback_mostrado="OK"
            )
        
        ajustar_dificultad_estudiante(self.user)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.nivel_dificultad_actual, 'Avanzado')
