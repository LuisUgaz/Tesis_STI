from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from AppTutoria.models import Tema
from AppEvaluar.models import Examen, Pregunta

class ExamenIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.docente = User.objects.create_user(username='docente_int', password='password')
        self.docente.is_staff = True
        self.docente.save()
        
        self.tema = Tema.objects.create(nombre="Geometría Integración")
        for i in range(10):
            Pregunta.objects.create(texto=f"Pregunta Int {i}", tema=self.tema)

    def test_flujo_completo_examen(self):
        """Prueba el flujo completo: Crear examen -> Verificar preguntas -> Eliminar examen -> Verificar liberación."""
        self.client.login(username='docente_int', password='password')
        
        # 1. Crear examen
        data = {
            'nombre': 'Examen Integrado',
            'tema': self.tema.id,
            'cantidad_preguntas': 5,
            'tiempo_limite': 30
        }
        response = self.client.post(reverse('evaluar:examen_create'), data)
        self.assertEqual(response.status_code, 302)
        
        # 2. Verificar que el examen tiene 5 preguntas
        examen = Examen.objects.get(nombre='Examen Integrado')
        self.assertEqual(examen.preguntas.count(), 5)
        
        # 3. Intentar crear otro examen pidiendo más preguntas de las que quedan (quedan 5)
        data_falla = {
            'nombre': 'Examen Fallido',
            'tema': self.tema.id,
            'cantidad_preguntas': 6,
            'tiempo_limite': 30
        }
        response = self.client.post(reverse('evaluar:examen_create'), data_falla)
        self.assertEqual(response.status_code, 200) # No redirige, vuelve al formulario con error
        form = response.context['form']
        self.assertIn('cantidad_preguntas', form.errors)
        self.assertEqual(form.errors['cantidad_preguntas'][0], 
                         f"No hay suficientes preguntas disponibles para el tema {self.tema.nombre}.")

        # 4. Eliminar el examen y verificar liberación
        preguntas_ids = list(examen.preguntas.values_list('id', flat=True))
        response = self.client.post(reverse('evaluar:examen_delete', args=[examen.id]))
        self.assertEqual(response.status_code, 302)
        
        for p_id in preguntas_ids:
            pregunta = Pregunta.objects.get(id=p_id)
            self.assertIsNone(pregunta.examen_tema)
        
        # 5. Ahora que se liberaron, debería poder crear un examen con 10 preguntas
        data_completo = {
            'nombre': 'Examen Final 10',
            'tema': self.tema.id,
            'cantidad_preguntas': 10,
            'tiempo_limite': 45
        }
        response = self.client.post(reverse('evaluar:examen_create'), data_completo)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Examen.objects.get(nombre='Examen Final 10').preguntas.count(), 10)
