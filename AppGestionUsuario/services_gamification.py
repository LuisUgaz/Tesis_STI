from django.db import transaction
from .models import Profile, Insignia, LogroEstudiante, MetricasEstudiante

# Constantes de puntaje
POINTS_EXERCISE_BASIC = 10
POINTS_EXERCISE_INTERMEDIATE = 20
POINTS_EXERCISE_ADVANCED = 30
POINTS_EXERCISE_FAIL = 2
POINTS_VIDEO = 5
POINTS_THEORY = 5
LEVEL_THRESHOLD = 100

class GamificationService:
    """Servicio centralizado para la asignación de puntos de experiencia e insignias"""

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
    def check_and_assign_badges(user):
        """
        Evalúa las reglas de insignias para un usuario y asigna las que correspondan.
        Retorna la lista de nuevas insignias obtenidas.
        """
        profile = user.profile
        logros_actuales = set(profile.logros.values_list('insignia__nombre', flat=True))
        insignias_disponibles = Insignia.objects.exclude(nombre__in=logros_actuales)
        
        nuevos_logros = []
        
        for insignia in insignias_disponibles:
            cumple = False
            
            if insignia.tipo_regla == 'HITOS':
                # Regla HITOS: Valor requerido es el número mínimo de registros de progreso
                count = user.progresos.count()
                if count >= insignia.valor_requerido:
                    cumple = True
            
            elif insignia.tipo_regla == 'DOMINIO':
                # Regla DOMINIO: Precisión general > valor_requerido
                metricas = MetricasEstudiante.objects.filter(usuario=user).first()
                if metricas and metricas.precision_general >= insignia.valor_requerido:
                    cumple = True
            
            elif insignia.tipo_regla == 'PROGRESION':
                # Regla PROGRESION: nivel_estudiante >= valor_requerido
                if profile.nivel_estudiante >= insignia.valor_requerido:
                    cumple = True
            
            # TODO: Implementar CONSTANCIA (requiere lógica de fechas)

            if cumple:
                LogroEstudiante.objects.create(perfil=profile, insignia=insignia)
                nuevos_logros.append(insignia)
                
        return nuevos_logros

    @staticmethod
    def _update_profile_gamification(user, points):
        """Actualiza atómicamente los puntos, nivel y evalúa insignias. Retorna (puntos, nuevas_insignias)"""
        with transaction.atomic():
            profile = Profile.objects.select_for_update().get(user=user)
            profile.puntos_acumulados += points
            
            # Lógica de niveles (HU23)
            nuevo_nivel = (profile.puntos_acumulados // LEVEL_THRESHOLD) + 1
            if nuevo_nivel > profile.nivel_estudiante:
                profile.nivel_estudiante = nuevo_nivel
            
            profile.save()
            
            # Evaluar insignias tras la actualización (HU24)
            nuevas_insignias = GamificationService.check_and_assign_badges(user)
            
        return points, nuevas_insignias
