from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from AppGestionUsuario.models import Profile, MetricasEstudiante
from AppTutoria.models import Tema
from AppEvaluar.models import Ejercicio, ResultadoEjercicio
from AppEvaluar.services_metrics import get_classroom_performance_summary
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

class ClassroomMetricsTest(TestCase):
    def setUp(self):
        # 1. Crear Tema y Usuarios
        self.tema = Tema.objects.create(nombre="Ángulos", slug="angulos")
        self.ej = Ejercicio.objects.create(tema=self.tema, texto="Q1", dificultad='Básico')
        
        # Estudiante 1 (5to A)
        self.user1 = User.objects.create_user(username='student1', password='pass')
        self.profile1 = Profile.objects.create(
            user=self.user1, rol='Estudiante', grado='5to', seccion='A', puntos_acumulados=100
        )
        # Crear resultados para que la agregación funcione (HU27 basa métricas en resultados reales)
        ResultadoEjercicio.objects.create(usuario=self.user1, ejercicio=self.ej, es_correcto=True, tiempo_empleado=10)

        # Estudiante 2 (5to A)
        self.user2 = User.objects.create_user(username='student2', password='pass')
        self.profile2 = Profile.objects.create(
            user=self.user2, rol='Estudiante', grado='5to', seccion='A', puntos_acumulados=200
        )
        # 40% precisión: 2 correctos de 5 intentos
        ResultadoEjercicio.objects.create(usuario=self.user2, ejercicio=self.ej, es_correcto=True, tiempo_empleado=10)
        ResultadoEjercicio.objects.create(usuario=self.user2, ejercicio=self.ej, es_correcto=True, tiempo_empleado=10)
        ResultadoEjercicio.objects.create(usuario=self.user2, ejercicio=self.ej, es_correcto=False, tiempo_empleado=10)
        ResultadoEjercicio.objects.create(usuario=self.user2, ejercicio=self.ej, es_correcto=False, tiempo_empleado=10)
        ResultadoEjercicio.objects.create(usuario=self.user2, ejercicio=self.ej, es_correcto=False, tiempo_empleado=10)
        # Student 1 (100%) + Student 2 (40%) = 140 / 2 = 70.


        # Estudiante 3 (5to B - Diferente sección)
        self.user3 = User.objects.create_user(username='student3', password='pass')
        self.profile3 = Profile.objects.create(
            user=self.user3, rol='Estudiante', grado='5to', seccion='B', puntos_acumulados=500
        )
        self.metricas3 = MetricasEstudiante.objects.create(
            usuario=self.user3, precision_general=100.0, dominio_por_tema={"Ángulos": 100.0}
        )

    def test_get_classroom_performance_summary(self):
        """Prueba que se calculen promedios correctos para una sección específica"""
        summary = get_classroom_performance_summary(grado='5to', seccion='A')
        
        # Promedio de precisión global: 3 aciertos / 6 intentos = 50%
        self.assertEqual(float(summary['precision_promedio']), 50.0)
        
        # Promedio de puntos: (100 + 200) / 2 = 150
        self.assertEqual(summary['puntos_promedio'], 150.0)
        
        # Total estudiantes: 2
        self.assertEqual(summary['total_estudiantes'], 2)

    def test_get_topic_performance_summary(self):
        """Prueba la agregación de dominio por tema en el aula"""
        summary = get_classroom_performance_summary(grado='5to', seccion='A')
        
        # Dominio promedio global en Ángulos: 3 aciertos / 6 intentos = 50%
        self.assertIn('Ángulos', summary['desempeno_por_tema'])
        self.assertEqual(summary['desempeno_por_tema']['Ángulos'], 50.0)

class TeacherReportsIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher = User.objects.create_user(username='teacher1', password='pass')
        Profile.objects.create(user=self.teacher, rol='Docente')
        
        self.tema = Tema.objects.create(nombre="Triángulos", slug="triangulos")
        self.student = User.objects.create_user(username='student_test', password='pass')
        Profile.objects.create(user=self.student, rol='Estudiante', grado='5to', seccion='A')
        
        # Resultado hace 10 días
        ej = Ejercicio.objects.create(tema=self.tema, texto="Q1", dificultad='Básico')
        from django.utils import timezone
        from datetime import timedelta
        res = ResultadoEjercicio.objects.create(
            usuario=self.student, ejercicio=ej, es_correcto=True, tiempo_empleado=10
        )
        res.fecha_resolucion = timezone.now() - timedelta(days=10)
        res.save()

    def test_json_endpoint_access_restricted(self):
        """Solo docentes pueden acceder al endpoint JSON"""
        self.client.login(username='student_test', password='pass')
        response = self.client.get(reverse('evaluar:reportes_data_json'))
        self.assertEqual(response.status_code, 403)

    def test_json_endpoint_date_filtering(self):
        """El endpoint JSON debe filtrar correctamente por fechas"""
        self.client.login(username='teacher1', password='pass')
        
        # Filtro de hoy (No debería encontrar el resultado de hace 10 días)
        hoy = timezone.now().date().isoformat()
        response = self.client.get(reverse('evaluar:reportes_data_json'), {'fecha_inicio': hoy})
        data = response.json()
        self.assertEqual(data['summary']['total_estudiantes'], 1)
        self.assertEqual(data['summary']['precision_promedio'], 0) # Sin resultados en el rango
        
        # Filtro incluyendo hace 10 días
        pasado = (timezone.now() - timedelta(days=15)).date().isoformat()
        response = self.client.get(reverse('evaluar:reportes_data_json'), {'fecha_inicio': pasado})
        data = response.json()
        self.assertEqual(data['summary']['precision_promedio'], 100.0)

    def test_json_endpoint_theme_filtering(self):
        """El endpoint JSON debe filtrar correctamente por tema específico"""
        self.client.login(username='teacher1', password='pass')
        
        # Crear otro tema y un resultado para él
        tema2 = Tema.objects.create(nombre="Ángulos", slug="angulos")
        ej2 = Ejercicio.objects.create(tema=tema2, texto="Q2", dificultad='Básico')
        # Resultado incorrecto para el tema 2
        ResultadoEjercicio.objects.create(
            usuario=self.student, ejercicio=ej2, es_correcto=False, tiempo_empleado=5
        )

        # Filtrar por Tema 1 (Triángulos) - Debería ser 100% precisión
        response = self.client.get(reverse('evaluar:reportes_data_json'), {'tema': self.tema.id})
        data = response.json()
        self.assertEqual(data['summary']['precision_promedio'], 100.0)
        self.assertIn('Triángulos', data['summary']['desempeno_por_tema'])
        self.assertNotIn('Ángulos', data['summary']['desempeno_por_tema'])

        # Filtrar por Tema 2 (Ángulos) - Debería ser 0% precisión
        response = self.client.get(reverse('evaluar:reportes_data_json'), {'tema': tema2.id})
        data = response.json()
        self.assertEqual(data['summary']['precision_promedio'], 0.0)
        self.assertIn('Ángulos', data['summary']['desempeno_por_tema'])
        self.assertNotIn('Triángulos', data['summary']['desempeno_por_tema'])

    def test_json_endpoint_combined_filtering(self):
        """Validar la combinación de múltiples filtros (Grado + Sección + Fecha + Tema)"""
        self.client.login(username='teacher1', password='pass')
        
        # Filtro que coincide con todo
        pasado = (timezone.now() - timedelta(days=15)).date().isoformat()
        params = {
            'grado': '5to',
            'seccion': 'A',
            'fecha_inicio': pasado,
            'tema': self.tema.id
        }
        response = self.client.get(reverse('evaluar:reportes_data_json'), params)
        data = response.json()
        self.assertEqual(data['summary']['total_estudiantes'], 1)
        self.assertEqual(data['summary']['precision_promedio'], 100.0)

        # Filtro que falla por sección
        params['seccion'] = 'B'
        response = self.client.get(reverse('evaluar:reportes_data_json'), params)
        data = response.json()
        self.assertEqual(data['summary']['total_estudiantes'], 0) # No hay estudiantes en 5to B

