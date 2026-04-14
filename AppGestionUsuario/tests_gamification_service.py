from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile
from .services_gamification import GamificationService

class GamificationServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teststudent', password='password123')
        self.profile = Profile.objects.create(
            user=self.user,
            nombres='Test',
            apellidos='Student',
            rol='Estudiante'
        )

    def test_assign_points_exercise_success_basic(self):
        """Prueba asignación de puntos por acierto en ejercicio nivel Básico"""
        puntos, insignias = GamificationService.assign_points_exercise(self.user, is_correct=True, difficulty='Básico')
        self.assertEqual(puntos, 10)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.puntos_acumulados, 10)

    def test_assign_points_exercise_success_intermediate(self):
        """Prueba asignación de puntos por acierto en ejercicio nivel Intermedio"""
        puntos, insignias = GamificationService.assign_points_exercise(self.user, is_correct=True, difficulty='Intermedio')
        self.assertEqual(puntos, 20)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.puntos_acumulados, 20)

    def test_assign_points_exercise_success_advanced(self):
        """Prueba asignación de puntos por acierto en ejercicio nivel Avanzado"""
        puntos, insignias = GamificationService.assign_points_exercise(self.user, is_correct=True, difficulty='Avanzado')
        self.assertEqual(puntos, 30)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.puntos_acumulados, 30)

    def test_assign_points_exercise_fail(self):
        """Prueba asignación de puntos mínimos por intento fallido"""
        puntos, insignias = GamificationService.assign_points_exercise(self.user, is_correct=False, difficulty='Avanzado')
        self.assertEqual(puntos, 2)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.puntos_acumulados, 2)

    def test_assign_points_video(self):
        """Prueba asignación de puntos por ver un video"""
        puntos, insignias = GamificationService.assign_points_video(self.user)
        self.assertEqual(puntos, 5)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.puntos_acumulados, 5)

    def test_assign_points_theory(self):
        """Prueba asignación de puntos por completar teoría"""
        puntos, insignias = GamificationService.assign_points_theory(self.user)
        self.assertEqual(puntos, 5)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.puntos_acumulados, 5)

    def test_cumulative_points(self):
        """Prueba que los puntos se acumulen correctamente en múltiples actividades"""
        GamificationService.assign_points_exercise(self.user, is_correct=True, difficulty='Básico') # 10
        GamificationService.assign_points_video(self.user) # 5
        GamificationService.assign_points_theory(self.user) # 5
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.puntos_acumulados, 20)

    def test_level_up_on_threshold(self):
        """Prueba que el nivel suba al alcanzar el umbral de 100 puntos"""
        # Sumar 100 puntos exactamente
        for _ in range(10):
            GamificationService.assign_points_exercise(self.user, is_correct=True, difficulty='Básico')
        
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.puntos_acumulados, 100)
        self.assertEqual(self.profile.nivel_estudiante, 2, "El nivel debería haber subido a 2")

    def test_no_level_up_before_threshold(self):
        """Prueba que el nivel no suba antes de alcanzar los 100 puntos"""
        # Sumar 90 puntos
        for _ in range(9):
            GamificationService.assign_points_exercise(self.user, is_correct=True, difficulty='Básico')
            
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.puntos_acumulados, 90)
        self.assertEqual(self.profile.nivel_estudiante, 1, "El nivel debería seguir siendo 1")

    def test_multiple_level_ups(self):
        """Prueba subidas de nivel consecutivas"""
        # Sumar 210 puntos (Debería ser nivel 3)
        for _ in range(7):
            GamificationService.assign_points_exercise(self.user, is_correct=True, difficulty='Avanzado') # 7 * 30 = 210
            
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.puntos_acumulados, 210)
        self.assertEqual(self.profile.nivel_estudiante, 3, "El nivel debería haber subido a 3")

