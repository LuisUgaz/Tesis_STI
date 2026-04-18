from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from AppGestionUsuario.models import Profile
from AppEvaluar.models import RecomendacionEstudiante
from .models import Tema

class ListaTemasViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('tutoria:lista_temas')
        
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

    def test_acceso_docente_permitido_lista(self):
        """Verifica que un docente pueda acceder a la lista de temas."""
        self.client.login(username='docente', password='password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

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

class TemaDetalleViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Crear usuarios
        self.user_estudiante = User.objects.create_user(username='estudiante', password='password123')
        Profile.objects.create(user=self.user_estudiante, rol='Estudiante', nombres='Est', apellidos='Test')
        
        self.user_docente = User.objects.create_user(username='docente', password='password123')
        Profile.objects.create(user=self.user_docente, rol='Docente', nombres='Doc', apellidos='Test')
        
        # Crear temas y contenido
        self.tema = Tema.objects.create(nombre="Ángulos", slug="angulos")
        from .models import ContenidoTema
        self.contenido = ContenidoTema.objects.create(
            tema=self.tema, 
            cuerpo_html="<h3>Teoría de Ángulos</h3><p>Contenido de prueba.</p>"
        )
        
        # URL del detalle
        self.url_detalle = reverse('tutoria:tema_detalle', kwargs={'slug': self.tema.slug})

    def test_acceso_anonimo_redirige_login(self):
        """Verifica que un usuario no autenticado sea redirigido."""
        response = self.client.get(self.url_detalle)
        self.assertEqual(response.status_code, 302)

    def test_acceso_docente_permitido(self):
        """Verifica que un docente PUEDA acceder al contenido de estudio (supervisión)."""
        self.client.login(username='docente', password='password123')
        response = self.client.get(self.url_detalle)
        self.assertEqual(response.status_code, 200)

    def test_acceso_estudiante_sin_recomendacion_redirige(self):
        """Verifica que un estudiante sea redirigido si no tiene recomendación."""
        self.client.login(username='estudiante', password='password123')
        response = self.client.get(self.url_detalle)
        self.assertRedirects(response, reverse('tutoria:lista_temas'))

    def test_acceso_estudiante_con_recomendacion_exitoso(self):
        """Verifica el acceso exitoso cuando el tema está recomendado (muestra resumen por defecto)."""
        self.client.login(username='estudiante', password='password123')
        
        # Crear recomendación
        RecomendacionEstudiante.objects.create(
            usuario=self.user_estudiante, 
            tema=self.tema.nombre,
            metrica_desempeno=40.0
        )
        
        response = self.client.get(self.url_detalle)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AppTutoria/tema_detalle.html')
        self.assertContains(response, "Resumen")

    def test_tema_no_existente_retorna_404(self):
        """Verifica que un slug inexistente retorne 404."""
        self.client.login(username='estudiante', password='password123')
        response = self.client.get("/tutoria/tema/no-existe/")
        self.assertEqual(response.status_code, 404)

    def test_acceso_detalle_muestra_resumen_por_defecto(self):
        """Verifica que al acceder al detalle se muestre el resumen por defecto."""
        self.client.login(username='estudiante', password='password123')
        RecomendacionEstudiante.objects.create(usuario=self.user_estudiante, tema=self.tema.nombre, metrica_desempeno=40.0)
        
        # Actualizar tema con descripción
        self.tema.descripcion = "Esta es la descripción del resumen."
        self.tema.save()
        
        response = self.client.get(self.url_detalle)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.tema.descripcion)
        self.assertEqual(response.context['seccion'], 'resumen')

    def test_acceso_detalle_teoria_muestra_contenido_teorico(self):
        """Verifica que al acceder con ?seccion=teoria se muestre el marco teórico."""
        self.client.login(username='estudiante', password='password123')
        RecomendacionEstudiante.objects.create(usuario=self.user_estudiante, tema=self.tema.nombre, metrica_desempeno=40.0)
        
        response = self.client.get(self.url_detalle + "?seccion=teoria")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Teoría de Ángulos")
        self.assertEqual(response.context['seccion'], 'teoria')

    def test_acceso_secciones_futuras_muestra_placeholder(self):
        """Verifica que las secciones futuras (ejercicios/videos) muestren un placeholder."""
        self.client.login(username='estudiante', password='password123')
        RecomendacionEstudiante.objects.create(usuario=self.user_estudiante, tema=self.tema.nombre, metrica_desempeno=40.0)
        
        for seccion in ['ejercicios', 'videos']:
            response = self.client.get(self.url_detalle + f"?seccion={seccion}")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context['seccion'], seccion)
            self.assertContains(response, "Próximamente")
