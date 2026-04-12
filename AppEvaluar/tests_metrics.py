from django.test import TestCase
from django.contrib.auth.models import User
from AppGestionUsuario.models import MetricasEstudiante
from .models import Ejercicio, ResultadoEjercicio, ExamenDiagnostico, ResultadoDiagnostico
from AppTutoria.models import Tema
from .services_metrics import actualizar_metricas_estudiante
from decimal import Decimal

class MetricsServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='metrics_student', password='password123')
        from AppGestionUsuario.models import Profile
        Profile.objects.create(user=self.user, rol='Estudiante', nombres='Test', apellidos='User', grado='2', seccion='A')
        self.tema = Tema.objects.create(nombre="TriÃ¡ngulos", slug="triangulos")
        self.ejercicio = Ejercicio.objects.create(tema=self.tema, texto="Test Ej", dificultad='BÃ¡sico')
        from .models import OpcionEjercicio
        self.opcion = OpcionEjercicio.objects.create(ejercicio=self.ejercicio, texto="Op 1", es_correcta=True)

    def test_view_validar_respuesta_updates_metrics(self):
        self.client.login(username='metrics_student', password='password123')
        from django.urls import reverse
        url = reverse('validar_respuesta')
        response = self.client.post(url, {
            'ejercicio_id': self.ejercicio.id,
            'opcion_id': self.opcion.id,
            'tiempo': 10
        })
        self.assertEqual(response.status_code, 200)
        
        # Verificar que se crearon las mÃ©tricas
        metricas = MetricasEstudiante.objects.get(usuario=self.user)
        self.assertEqual(metricas.precision_general, Decimal('100.00'))
        self.assertEqual(metricas.dominio_por_tema["TriÃ¡ngulos"], 100.0)

    def test_precision_calculation_incremental(self):
        # 1. Primera actividad (correcta)
        res1 = ResultadoEjercicio.objects.create(
            usuario=self.user, ejercicio=self.ejercicio, es_correcto=True,
            tiempo_empleado=10, feedback_mostrado="Bien"
        )
        actualizar_metricas_estudiante(self.user, res1)
        metricas = MetricasEstudiante.objects.get(usuario=self.user)
        self.assertEqual(metricas.precision_general, Decimal('100.00'))

        # 2. Segunda actividad (incorrecta)
        res2 = ResultadoEjercicio.objects.create(
            usuario=self.user, ejercicio=self.ejercicio, es_correcto=False,
            tiempo_empleado=15, feedback_mostrado="Mal"
        )
        actualizar_metricas_estudiante(self.user, res2)
        metricas.refresh_from_db()
        self.assertEqual(metricas.precision_general, Decimal('50.00'))

    def test_rendimiento_calculation_from_diagnostico(self):
        examen = ExamenDiagnostico.objects.create(nombre="Examen 1")
        res_diag = ResultadoDiagnostico.objects.create(
            estudiante=self.user, examen=examen, puntaje=Decimal('80.00')
        )
        actualizar_metricas_estudiante(self.user, res_diag)
        metricas = MetricasEstudiante.objects.get(usuario=self.user)
        self.assertEqual(metricas.rendimiento_academico, Decimal('80.00'))
        
        # Otro examen
        examen2 = ExamenDiagnostico.objects.create(nombre="Examen 2")
        res_diag2 = ResultadoDiagnostico.objects.create(
            estudiante=self.user, examen=examen2, puntaje=Decimal('60.00')
        )
        actualizar_metricas_estudiante(self.user, res_diag2)
        metricas.refresh_from_db()
        self.assertEqual(metricas.rendimiento_academico, Decimal('70.00'))

    def test_tiempo_promedio_calculation(self):
        # 1. 10 segundos
        res1 = ResultadoEjercicio.objects.create(
            usuario=self.user, ejercicio=self.ejercicio, es_correcto=True,
            tiempo_empleado=10, feedback_mostrado="Bien"
        )
        actualizar_metricas_estudiante(self.user, res1)
        
        # 2. 20 segundos
        res2 = ResultadoEjercicio.objects.create(
            usuario=self.user, ejercicio=self.ejercicio, es_correcto=False,
            tiempo_empleado=20, feedback_mostrado="Mal"
        )
        actualizar_metricas_estudiante(self.user, res2)
        
        metricas = MetricasEstudiante.objects.get(usuario=self.user)
        self.assertEqual(metricas.tiempo_respuesta_promedio, Decimal('15.00'))

    def test_dominio_por_tema_calculation(self):
        # Tema 1: TriÃ¡ngulos (1 correcto, 1 incorrecto -> 50%)
        res1 = ResultadoEjercicio.objects.create(
            usuario=self.user, ejercicio=self.ejercicio, es_correcto=True,
            tiempo_empleado=10, feedback_mostrado="Bien"
        )
        actualizar_metricas_estudiante(self.user, res1)
        
        res2 = ResultadoEjercicio.objects.create(
            usuario=self.user, ejercicio=self.ejercicio, es_correcto=False,
            tiempo_empleado=10, feedback_mostrado="Mal"
        )
        actualizar_metricas_estudiante(self.user, res2)
        
        # Tema 2: Ãngulos (1 correcto -> 100%)
        tema2 = Tema.objects.create(nombre="Ãngulos", slug="angulos")
        ej2 = Ejercicio.objects.create(tema=tema2, texto="Ej 2", dificultad='BÃ¡sico')
        res3 = ResultadoEjercicio.objects.create(
            usuario=self.user, ejercicio=ej2, es_correcto=True,
            tiempo_empleado=10, feedback_mostrado="Bien"
        )
        actualizar_metricas_estudiante(self.user, res3)
        
        metricas = MetricasEstudiante.objects.get(usuario=self.user)
        self.assertEqual(metricas.dominio_por_tema["TriÃ¡ngulos"], 50.0)
        self.assertEqual(metricas.dominio_por_tema["Ãngulos"], 100.0)
