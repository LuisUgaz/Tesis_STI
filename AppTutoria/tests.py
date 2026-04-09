from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from AppGestionUsuario.models import Profile
from AppEvaluar.models import RecomendacionEstudiante
from .models import Tema

class ListaTemasViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='student', password='password')
        Profile.objects.create(user=self.user, rol='Estudiante')
        self.client.login(username='student', password='password')
        
        # Crear temas en la BD para que las pruebas no fallen por falta de datos
        self.temas_nombres = ['Triángulos', 'Ángulos', 'Segmentos', 'Rectas', 'Geometría Plana']
        for nombre in self.temas_nombres:
            Tema.objects.create(nombre=nombre)

    def test_lista_temas_view_status_code(self):
        """La vista debe retornar 200 OK para un usuario autenticado."""
        url = reverse('lista_temas')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_lista_temas_context_con_recomendacion(self):
        """Si el usuario tiene recomendación, debe estar en el contexto y ser la primera."""
        t_fav = 'Ángulos'
        RecomendacionEstudiante.objects.create(
            usuario=self.user,
            tema=t_fav,
            metrica_desempeno=25.0
        )
        
        url = reverse('lista_temas')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('recomendacion', response.context)
        self.assertEqual(response.context['recomendacion'].tema, t_fav)
        
        # El primer tema en la lista 'temas' debe ser el recomendado
        temas = response.context['temas']
        self.assertEqual(temas[0].nombre, t_fav)

    def test_lista_temas_context_sin_recomendacion(self):
        """Si no hay recomendación, el contexto debe reflejarlo."""
        url = reverse('lista_temas')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context.get('recomendacion'))
        
        # La lista de temas debe estar completa
        self.assertIn('temas', response.context)
        self.assertEqual(len(response.context['temas']), 5)
