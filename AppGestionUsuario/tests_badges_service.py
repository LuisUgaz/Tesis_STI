from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, Insignia, LogroEstudiante, MetricasEstudiante
from AppTutoria.models import Tema, ProgresoEstudiante
from .services_gamification import GamificationService

class BadgesServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='badgestudent', password='password123')
        self.profile = Profile.objects.create(
            user=self.user,
            nombres='Badge',
            apellidos='Student',
            rol='Estudiante',
            grado='5to',
            seccion='A'
        )
        self.metricas = MetricasEstudiante.objects.create(usuario=self.user)
        self.tema = Tema.objects.create(nombre="Triángulos", slug="triangulos")
        
        # Obtener insignias creadas por migración de datos
        self.b_welcome = Insignia.objects.get(nombre="Primeros Pasos")
        self.b_master = Insignia.objects.get(nombre="Maestro de Triángulos")
        self.b_veteran = Insignia.objects.get(nombre="Veterano (Nivel 5)")

    def test_assign_welcome_badge(self):
        """Prueba que se asigne la insignia de bienvenida tras completar una actividad"""
        # Crear progreso (HITOS requiere al menos 1 progreso)
        ProgresoEstudiante.objects.create(
            usuario=self.user, tema=self.tema, tipo_actividad='Ejercicio',
            grado='5to', seccion='A'
        )
        
        # Al asignar puntos, se debe evaluar insignias
        GamificationService.assign_points_exercise(self.user, is_correct=True, difficulty='Básico')
        
        self.assertEqual(self.profile.logros.count(), 1)
        self.assertTrue(self.profile.logros.filter(insignia=self.b_welcome).exists())

    def test_no_duplicate_badges(self):
        """Prueba que no se asigne la misma insignia dos veces"""
        ProgresoEstudiante.objects.create(
            usuario=self.user, tema=self.tema, tipo_actividad='Ejercicio',
            grado='5to', seccion='A'
        )
        
        GamificationService.assign_points_exercise(self.user, is_correct=True, difficulty='Básico')
        GamificationService.assign_points_exercise(self.user, is_correct=True, difficulty='Básico')
        
        self.assertEqual(self.profile.logros.count(), 1)

    def test_domain_badge_assignment(self):
        """Prueba asignación por precisión > 80%"""
        # Simulamos que el estudiante alcanza 85% de precisión
        self.metricas.precision_general = 85.0
        self.metricas.save()
        
        # Evaluamos reglas
        nuevas = GamificationService.check_and_assign_badges(self.user)
        
        self.assertIn(self.b_master, nuevas)
        self.assertTrue(self.profile.logros.filter(insignia=self.b_master).exists())

    def test_progression_badge_assignment(self):
        """Prueba asignación por alcanzar nivel 5"""
        self.profile.nivel_estudiante = 5
        self.profile.save()
        
        nuevas = GamificationService.check_and_assign_badges(self.user)
        
        self.assertIn(self.b_veteran, nuevas)
        self.assertTrue(self.profile.logros.filter(insignia=self.b_veteran).exists())
