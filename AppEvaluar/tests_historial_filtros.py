from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from AppGestionUsuario.models import Profile
from AppTutoria.models import Tema, ProgresoEstudiante
from django.utils import timezone
from datetime import timedelta

class HistorialFiltrosTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='student_filter', password='password123')
        Profile.objects.create(user=self.user, nombres='Juan', apellidos='Filtro', rol='Estudiante')
        self.client.login(username='student_filter', password='password123')

        self.tema1 = Tema.objects.create(nombre="Triángulos", slug="triangulos")
        self.tema2 = Tema.objects.create(nombre="Ángulos", slug="angulos")

        # Crear progresos en diferentes fechas
        self.hoy = timezone.now()
        self.ayer = self.hoy - timedelta(days=1)
        self.hace_una_semana = self.hoy - timedelta(days=7)

        # Progreso Hoy (Tema 1)
        self.p1 = ProgresoEstudiante.objects.create(
            usuario=self.user, tema=self.tema1, tipo_actividad='Ejercicio',
            grado='2', seccion='A'
        )
        # Forzar fecha_registro (ya que es auto_now_add)
        ProgresoEstudiante.objects.filter(id=self.p1.id).update(fecha_registro=self.hoy)

        # Progreso Ayer (Tema 2)
        self.p2 = ProgresoEstudiante.objects.create(
            usuario=self.user, tema=self.tema2, tipo_actividad='Video',
            grado='2', seccion='A'
        )
        ProgresoEstudiante.objects.filter(id=self.p2.id).update(fecha_registro=self.ayer)

        # Progreso Hace una semana (Tema 1)
        self.p3 = ProgresoEstudiante.objects.create(
            usuario=self.user, tema=self.tema1, tipo_actividad='Teoría',
            grado='2', seccion='A'
        )
        ProgresoEstudiante.objects.filter(id=self.p3.id).update(fecha_registro=self.hace_una_semana)

        self.url = reverse('historial_resultados')

    def test_filter_by_date_range_start(self):
        """Probar filtrado solo con fecha de inicio."""
        fecha_inicio = self.ayer.date().isoformat()
        response = self.client.get(self.url, {'fecha_inicio': fecha_inicio})
        progresos = response.context['progresos']
        # Debería mostrar Hoy y Ayer (2 registros)
        self.assertEqual(progresos.count(), 2)
        self.assertIn(self.p1, progresos)
        self.assertIn(self.p2, progresos)
        self.assertNotIn(self.p3, progresos)

    def test_filter_by_date_range_end(self):
        """Probar filtrado solo con fecha de fin."""
        fecha_fin = self.ayer.date().isoformat()
        response = self.client.get(self.url, {'fecha_fin': fecha_fin})
        progresos = response.context['progresos']
        # Debería mostrar Ayer y Hace una semana (2 registros)
        self.assertEqual(progresos.count(), 2)
        self.assertIn(self.p2, progresos)
        self.assertIn(self.p3, progresos)
        self.assertNotIn(self.p1, progresos)

    def test_filter_by_date_range_full(self):
        """Probar filtrado con rango de fechas completo (Ayer)."""
        fecha_inicio = self.ayer.date().isoformat()
        fecha_fin = self.ayer.date().isoformat()
        response = self.client.get(self.url, {'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin})
        progresos = response.context['progresos']
        # Debería mostrar solo Ayer (1 registro)
        self.assertEqual(progresos.count(), 1)
        self.assertIn(self.p2, progresos)

    def test_filter_combined_tema_and_date(self):
        """Probar filtrado combinado de tema y fecha."""
        fecha_inicio = self.hace_una_semana.date().isoformat()
        fecha_fin = self.ayer.date().isoformat()
        # Filtrar por Tema 2 (Ángulos) en ese rango -> solo Ayer (p2)
        response = self.client.get(self.url, {
            'tema': self.tema2.id,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin
        })
        progresos = response.context['progresos']
        self.assertEqual(progresos.count(), 1)
        self.assertIn(self.p2, progresos)
        self.assertNotIn(self.p3, progresos) # p3 es Tema 1

    def test_filter_no_results(self):
        """Probar comportamiento cuando no hay resultados en el rango."""
        fecha_inicio = (self.hoy + timedelta(days=10)).date().isoformat()
        response = self.client.get(self.url, {'fecha_inicio': fecha_inicio})
        progresos = response.context['progresos']
        self.assertEqual(progresos.count(), 0)
        # Verificar mensaje de alerta en HTML
        self.assertContains(response, "No se encontraron resultados para los filtros aplicados.")

    def test_filter_form_rendering(self):
        """Verificar que los inputs de fecha están en el HTML."""
        response = self.client.get(self.url)
        self.assertContains(response, 'type="date" name="fecha_inicio"')
        self.assertContains(response, 'type="date" name="fecha_fin"')
        self.assertContains(response, '<option value="desc" selected>Reciente</option>')

    def test_filter_persistence_in_form(self):
        """Verificar que los valores de los filtros se mantienen tras la recarga."""
        fecha_inicio = self.ayer.date().isoformat()
        response = self.client.get(self.url, {'fecha_inicio': fecha_inicio, 'tema': self.tema1.id})
        self.assertContains(response, f'value="{fecha_inicio}"')
        self.assertContains(response, f'value="{self.tema1.id}" selected')
