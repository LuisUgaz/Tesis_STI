from django.db import transaction
from .models import Profile

# Constantes de puntaje
POINTS_EXERCISE_BASIC = 10
POINTS_EXERCISE_INTERMEDIATE = 20
POINTS_EXERCISE_ADVANCED = 30
POINTS_EXERCISE_FAIL = 2
POINTS_VIDEO = 5
POINTS_THEORY = 5
LEVEL_THRESHOLD = 100

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

        return GamificationService._update_profile_gamification(user, points)

    @staticmethod
    def assign_points_video(user):
        """Asigna puntos fijos por visualización de video"""
        return GamificationService._update_profile_gamification(user, POINTS_VIDEO)

    @staticmethod
    def assign_points_theory(user):
        """Asigna puntos fijos por completar lectura de teoría"""
        return GamificationService._update_profile_gamification(user, POINTS_THEORY)

    @staticmethod
    def _update_profile_gamification(user, points):
        """Actualiza atómicamente los puntos y el nivel en el perfil del usuario"""
        with transaction.atomic():
            profile = Profile.objects.select_for_update().get(user=user)
            profile.puntos_acumulados += points
            
            # Lógica de niveles (HU23): nivel = (puntos // umbral) + 1
            nuevo_nivel = (profile.puntos_acumulados // LEVEL_THRESHOLD) + 1
            if nuevo_nivel > profile.nivel_estudiante:
                profile.nivel_estudiante = nuevo_nivel
            
            profile.save()
        return points

    @staticmethod
    def _update_profile_points(user, points):
        """OBSOLETO: Usar _update_profile_gamification en su lugar"""
        return GamificationService._update_profile_gamification(user, points)
