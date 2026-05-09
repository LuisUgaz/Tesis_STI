from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail
from AppGestionUsuario.forms import ContactoForm

class ContactoFormTests(TestCase):
    def test_form_valid_data(self):
        """Prueba que el formulario sea válido con datos correctos."""
        form = ContactoForm(data={
            'asunto': 'Duda sobre geometría',
            'mensaje': 'Hola, tengo una duda sobre los triángulos.'
        })
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        """Prueba que el formulario sea inválido si faltan campos obligatorios."""
        form = ContactoForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)
        self.assertIn('asunto', form.errors)
        self.assertIn('mensaje', form.errors)

    def test_form_optional_context(self):
        """Prueba que el formulario acepte campos de contexto opcionales."""
        form = ContactoForm(data={
            'asunto': 'Duda específica',
            'mensaje': 'Duda sobre el ejercicio.',
            'tema_id': 1,
            'ejercicio_id': 10
        })
        self.assertTrue(form.is_valid())

class ContactoViewTests(TestCase):
    def setUp(self):
        self.username = 'estudiante1'
        self.password = 'Password123!'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
            email='estudiante@ejemplo.com'
        )
        self.contacto_url = reverse('contacto')

    def test_view_login_required(self):
        """Prueba que se requiera inicio de sesión para acceder al formulario."""
        response = self.client.get(self.contacto_url)
        # Redirige al login si no está autenticado
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_view_render_authenticated(self):
        """Prueba que el formulario se renderice correctamente para un usuario autenticado."""
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.contacto_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AppGestionUsuario/contacto.html')
        self.assertIsInstance(response.context['form'], ContactoForm)

    def test_view_send_email_success(self):
        """Prueba el envío exitoso de una consulta por correo."""
        self.client.login(username=self.username, password=self.password)
        data = {
            'asunto': 'Consulta de Prueba',
            'mensaje': 'Este es un mensaje de prueba desde los tests.'
        }
        response = self.client.post(self.contacto_url, data)
        
        # Redirección tras éxito (podría ser a 'home' o a la misma página)
        self.assertEqual(response.status_code, 302)
        
        # Verificar que se envió un correo
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.subject, 'Consulta de Prueba')
        self.assertIn('Este es un mensaje de prueba', email.body)
        self.assertIn(self.user.username, email.body)
        self.assertEqual(email.to, ['luisugaz63@gmail.com'])

    def test_view_send_email_with_context(self):
        """Prueba el envío de correo incluyendo el contexto del tema/ejercicio."""
        self.client.login(username=self.username, password=self.password)
        data = {
            'asunto': 'Consulta con Contexto',
            'mensaje': 'Duda sobre el tema 5.',
            'tema_id': 5
        }
        response = self.client.post(self.contacto_url, data)
        self.assertEqual(response.status_code, 302)
        
        # Verificar el contenido del correo
        email = mail.outbox[0]
        self.assertIn('ID del Tema: 5', email.body)
