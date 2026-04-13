from django.db import transaction
from .models import Profile

# Constantes de puntaje
POINTS_EXERCISE_BASIC = 10
POINTS_EXERCISE_INTERMEDIATE = 20
POINTS_EXERCISE_ADVANCED = 30
POINTS_EXERCISE_FAIL = 2
POINTS_VIDEO = 5
POINTS_THEORY = 5

class GamificationService:
    """Servicio centralizado para la asignación de puntos de experiencia"""

    @staticmethod
    def assign_points_exercise(user, is_correct, difficulty):
        """Asigna puntos por resolución de ejercicios según dificultad y resultado"""
        if not is_correct:
            points = POINTS_EXERCISE_FAIL
        elif difficulty == 'Básico':
            points = POINTS_EXERCISE_BASIC
        elif difficulty == 'Intermedio':
            points = POINTS_EXERCISE_INTERMEDIATE
        elif difficulty == 'Avanzado':
            points = POINTS_EXERCISE_ADVANCED
        else:
            points = POINTS_EXERCISE_FAIL

        return GamificationService._update_profile_points(user, points)

    @staticmethod
    def assign_points_video(user):
        """Asigna puntos fijos por visualización de video"""
        return GamificationService._update_profile_points(user, POINTS_VIDEO)

    @staticmethod
    def assign_points_theory(user):
        """Asigna puntos fijos por completar lectura de teoría"""
        return GamificationService._update_profile_points(user, POINTS_THEORY)

    @staticmethod
    def _update_profile_points(user, points):
        """Actualiza atómicamente los puntos acumulados en el perfil del usuario"""
        with transaction.atomic():
            profile = Profile.objects.select_for_update().get(user=user)
            profile.puntos_acumulados += points
            profile.save()
        return points
