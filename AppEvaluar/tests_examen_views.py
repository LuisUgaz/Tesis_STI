from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from AppTutoria.models import Tema
from AppEvaluar.models import Examen, Pregunta

class ExamenViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Crear docente
        self.docente = User.objects.create_user(username='docente', password='password')
        self.docente.is_staff = True # Asumiendo que is_staff identifica al docente por ahora
        self.docente.save()
        
        # Crear estudiante (no debería tener acceso)
        self.estudiante = User.objects.create_user(username='estudiante', password='password')
        
        self.tema = Tema.objects.create(nombre="Geometría")
        for i in range(5):
            Pregunta.objects.create(texto=f"P{i}", tema=self.tema)

    def test_acceso_docente_dashboard(self):
        """Verificar que solo el docente puede acceder al dashboard de exámenes."""
        self.client.login(username='docente', password='password')
        response = self.client.get(reverse('evaluar:examen_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_acceso_estudiante_denegado(self):
        """Verificar que el estudiante no tiene acceso al dashboard."""
        self.client.login(username='estudiante', password='password')
        response = self.client.get(reverse('evaluar:examen_dashboard'))
        self.assertEqual(response.status_code, 403) # O redirección, según política

    def test_creacion_examen_view(self):
        """Verificar la creación de un examen a través de la vista."""
        self.client.login(username='docente', password='password')
        data = {
            'nombre': 'Examen Final Geometría',
            'tema': self.tema.id,
            'cantidad_preguntas': 3,
            'tiempo_limite': 60
        }
        response = self.client.post(reverse('evaluar:examen_create'), data)
        self.assertEqual(response.status_code, 302) # Redirección tras éxito
        self.assertTrue(Examen.objects.filter(nombre='Examen Final Geometría').exists())
        examen = Examen.objects.get(nombre='Examen Final Geometría')
        self.assertEqual(examen.preguntas.count(), 3)

    def test_eliminacion_examen_view(self):
        """Verificar la eliminación de un examen."""
        examen = Examen.objects.create(
            nombre='Examen a borrar',
            tema=self.tema,
            cantidad_preguntas=2,
            tiempo_limite=45
        )
        self.client.login(username='docente', password='password')
        response = self.client.post(reverse('evaluar:examen_delete', args=[examen.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Examen.objects.filter(id=examen.id).exists())

    def test_actualizacion_examen_view(self):
        """Verificar que el docente puede actualizar el tema de un examen."""
        # 1. Crear examen inicial
        examen = Examen.objects.create(
            nombre='Examen Inicial',
            tema=self.tema,
            cantidad_preguntas=2,
            tiempo_limite=45
        )
        
        # 2. Crear un nuevo tema
        nuevo_tema = Tema.objects.create(nombre="Trigonometría")
        Pregunta.objects.create(texto="P_Tri1", tema=nuevo_tema)
        Pregunta.objects.create(texto="P_Tri2", tema=nuevo_tema)
        
        # 3. Datos de actualización
        data = {
            'nombre': 'Examen Actualizado',
            'tema': nuevo_tema.id,
            'cantidad_preguntas': 2,
            'tiempo_limite': 30
        }
        
        self.client.login(username='docente', password='password')
        response = self.client.post(reverse('evaluar:examen_update', args=[examen.id]), data)
        self.assertEqual(response.status_code, 302)
        
        # 4. Verificar cambios
        examen.refresh_from_db()
        self.assertEqual(examen.nombre, 'Examen Actualizado')
        self.assertEqual(examen.tema, nuevo_tema)
        self.assertEqual(examen.tiempo_limite, 30)
