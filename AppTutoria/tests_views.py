from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from AppGestionUsuario.models import Profile
from AppEvaluar.models import RecomendacionEstudiante
from .models import Tema

class ListaTemasViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('lista_temas')
        
        # Crear usuario estudiante
        self.user_estudiante = User.objects.create_user(username='estudiante', password='password123')
        self.profile_estudiante = Profile.objects.create(user=self.user_estudiante, rol='Estudiante')
        
        # Crear usuario docente
        self.user_docente = User.objects.create_user(username='docente', password='password123')
        self.profile_docente = Profile.objects.create(user=self.user_docente, rol='Docente')
        
        # Crear algunos temas
        Tema.objects.create(nombre="Triángulos")
        Tema.objects.create(nombre="Ángulos")

    def test_acceso_estudiante_autenticado(self):
        """Verifica que un estudiante autenticado pueda acceder a la lista de temas."""
        self.client.login(username='estudiante', password='password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AppTutoria/lista_temas.html')

    def test_acceso_docente_restringido(self):
        """Verifica que un docente sea redirigido o se le niegue el acceso (dependiendo de la implementación, aquí esperamos un 403 o redirección)."""
        self.client.login(username='docente', password='password123')
        response = self.client.get(self.url)
        # Por ahora, si no tiene el rol, podemos redirigir al home o mostrar 403. 
        # Vamos a implementar que solo Estudiantes pasen.
        self.assertEqual(response.status_code, 403)

    def test_acceso_anonimo_restringido(self):
        """Verifica que un usuario no autenticado sea redirigido al login."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302) # Redirección a login

    def test_reordenamiento_tema_recomendado(self):
        """Verifica que el tema recomendado aparezca primero en la lista."""
        self.client.login(username='estudiante', password='password123')
        
        # Crear recomendación para 'Ángulos' (que no es el primero por defecto)
        RecomendacionEstudiante.objects.create(
            usuario=self.user_estudiante, 
            tema="Ángulos",
            metrica_desempeno=40.0
        )
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
        temas_en_contexto = response.context['temas']
        self.assertEqual(temas_en_contexto[0].nombre, "Ángulos")
