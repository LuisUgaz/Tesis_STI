from django.test import TestCase
from django.contrib.auth.models import User
from AppTutoria.models import Tema, VideoTema, VisualizacionVideo, ProgresoEstudiante
from AppEvaluar.models import (
    ResultadoDiagnostico, RecomendacionEstudiante, 
    ResultadoExamen, ControlPracticaTema, Examen,
    ExamenDiagnostico
)
from AppTutoria.utils import verificar_completitud_tema, validar_estado_acceso_tema

class ValidacionCompletitudTest(TestCase):
    def setUp(self):
        # Crear usuario y perfil
        self.user = User.objects.create_user(username='estudiante_test', password='password123')
        from AppGestionUsuario.models import Profile
        self.profile = Profile.objects.create(user=self.user, rol='Estudiante')
        
        # Crear Temas
        self.tema_rec = Tema.objects.create(nombre='Tema Recomendado', slug='tema-rec')
        self.tema_otro = Tema.objects.create(nombre='Otro Tema', slug='otro-tema')
        
        # Recomendación (Añadido metrica_desempeno para cumplir con integridad)
        RecomendacionEstudiante.objects.create(
            usuario=self.user, 
            tema=self.tema_rec.nombre,
            metrica_desempeno=0.0
        )
        # Diagnóstico (necesario para pasar el primer filtro de validar_estado_acceso_tema)
        examen_diag = ExamenDiagnostico.objects.create(nombre="Diagnóstico Inicial", descripcion="Test")
        ResultadoDiagnostico.objects.create(estudiante=self.user, examen=examen_diag, puntaje=50.0)

    def test_verificar_completitud_teoria_pendiente(self):
        """Si la teoría no está al 100%, el tema no está completo."""
        completado, mensaje = verificar_completitud_tema(self.user, self.tema_rec)
        self.assertFalse(completado)
        self.assertIn("Falta completar el material teórico", mensaje)

    def test_verificar_completitud_videos_pendientes(self):
        """Si hay videos activos y no se han visto todos, el tema no está completo."""
        # Teoría al 100%
        ProgresoEstudiante.objects.create(
            usuario=self.user, tema=self.tema_rec, 
            tipo_actividad='Teoría', porcentaje_completado=100.0
        )
        
        # Crear un video
        video = VideoTema.objects.create(tema=self.tema_rec, titulo="Video 1", es_activo=True)
        
        completado, mensaje = verificar_completitud_tema(self.user, self.tema_rec)
        self.assertFalse(completado)
        self.assertIn("Falta visualizar todos los videos", mensaje)

    def test_verificar_completitud_practica_bloqueada(self):
        """Si la práctica no está desbloqueada (examen_desbloqueado=False), el tema no está completo."""
        # Teoría y Videos OK
        ProgresoEstudiante.objects.create(
            usuario=self.user, tema=self.tema_rec, 
            tipo_actividad='Teoría', porcentaje_completado=100.0
        )
        
        completado, mensaje = verificar_completitud_tema(self.user, self.tema_rec)
        self.assertFalse(completado)
        self.assertIn("Falta completar la sesión de práctica", mensaje)

    def test_verificar_completitud_examenes_insuficientes(self):
        """Si tiene menos de 4 exámenes aprobados, el tema no está completo."""
        # Teoría, Videos y Práctica OK
        ProgresoEstudiante.objects.create(
            usuario=self.user, tema=self.tema_rec, 
            tipo_actividad='Teoría', porcentaje_completado=100.0
        )
        ControlPracticaTema.objects.create(usuario=self.user, tema=self.tema_rec, examen_desbloqueado=True)
        
        # Crear 3 exámenes aprobados
        for i in range(3):
            ex = Examen.objects.create(
                tema=self.tema_rec, 
                nombre=f"Examen {i}",
                cantidad_preguntas=10,
                tiempo_limite=20
            )
            ResultadoExamen.objects.create(estudiante=self.user, examen=ex, puntaje=80.0)
            
        completado, mensaje = verificar_completitud_tema(self.user, self.tema_rec)
        self.assertFalse(completado)
        self.assertIn("Debes aprobar al menos 4 exámenes", mensaje)

    def test_verificar_completitud_total_exito(self):
        """Si cumple todos los requisitos, el tema está completo."""
        # 1. Teoría 100%
        ProgresoEstudiante.objects.create(
            usuario=self.user, tema=self.tema_rec, 
            tipo_actividad='Teoría', porcentaje_completado=100.0
        )
        # 2. Videos (ninguno activo para este test, se da por cumplido)
        # 3. Práctica desbloqueada
        ControlPracticaTema.objects.create(usuario=self.user, tema=self.tema_rec, examen_desbloqueado=True)
        # 4. 4 exámenes aprobados
        for i in range(4):
            ex = Examen.objects.create(
                tema=self.tema_rec, 
                nombre=f"Examen Final {i}",
                cantidad_preguntas=10,
                tiempo_limite=20
            )
            ResultadoExamen.objects.create(estudiante=self.user, examen=ex, puntaje=75.0)
            
        completado, mensaje = verificar_completitud_tema(self.user, self.tema_rec)
        self.assertTrue(completado)
        self.assertEqual(mensaje, "Tema completado.")

    def test_validar_estado_acceso_bloqueado_por_recomendacion(self):
        """Si intenta acceder a otro tema sin terminar el recomendado, debe retornar TEMA_PENDIENTE."""
        permitido, error_code, tema_pendiente = validar_estado_acceso_tema(self.user, self.tema_otro)
        self.assertFalse(permitido)
        self.assertEqual(error_code, 'TEMA_PENDIENTE')
        self.assertEqual(tema_pendiente, self.tema_rec.nombre)

    def test_validar_estado_acceso_permitido_mismo_tema(self):
        """Acceder al tema recomendado siempre está permitido."""
        permitido, error_code, tema_pendiente = validar_estado_acceso_tema(self.user, self.tema_rec)
        self.assertTrue(permitido)
        self.assertIsNone(error_code)
