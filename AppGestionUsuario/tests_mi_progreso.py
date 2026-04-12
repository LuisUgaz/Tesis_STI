from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile, MetricasEstudiante

class MiProgresoViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='student_metrics', password='password123')
        self.profile = Profile.objects.create(user=self.user, rol='Estudiante', nombres='Juan', apellidos='Perez')
        
        # Crear mÃ©tricas de prueba
        self.metricas = MetricasEstudiante.objects.create(
            usuario=self.user,
            precision_general=75.5,
            rendimiento_academico=80.0,
            tiempo_respuesta_promedio=15.2,
            dominio_por_tema={"TriÃ¡ngulos": 80.0, "Ãngulos": 60.0}
        )
        
        self.url = reverse('mi_progreso')

    def test_mi_progreso_requires_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302) # Redirect to login

    def test_mi_progreso_requires_student_role(self):
        # Crear un docente
        docente = User.objects.create_user(username='teacher_user', password='password123')
        Profile.objects.create(user=docente, rol='Docente', nombres='Profe', apellidos='X')
        
        self.client.login(username='teacher_user', password='password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403) # Forbidden or PermissionDenied

    def test_mi_progreso_shows_correct_data(self):
        self.client.login(username='student_metrics', password='password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AppGestionUsuario/mi_progreso.html')
        
        # Verificar datos en contexto
        metricas_context = response.context['metricas']
        self.assertEqual(metricas_context.precision_general, 75.5)
        self.assertEqual(metricas_context.dominio_por_tema["TriÃ¡ngulos"], 80.0)
