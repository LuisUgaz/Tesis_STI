from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from AppGestionUsuario.models import Profile, Insignia

class BadgeManagementViewsTest(TestCase):
    def setUp(self):
        # Crear usuarios con diferentes roles
        self.admin_user = User.objects.create_user(username='admin', password='password123')
        Profile.objects.create(user=self.admin_user, rol='Administrador', nombres='Admin', apellidos='User')
        
        self.estudiante_user = User.objects.create_user(username='estudiante', password='password123')
        Profile.objects.create(user=self.estudiante_user, rol='Estudiante', nombres='Est', apellidos='User')
        
        # Crear una insignia de prueba
        self.insignia = Insignia.objects.create(
            nombre='Prueba',
            descripcion='Desc',
            icono_clase='fas fa-medal',
            tipo_regla='HITOS',
            valor_requerido=1
        )

    def test_access_restricted_to_admin(self):
        """Verificar que solo administradores pueden acceder."""
        get_urls = [
            reverse('admin_badge_list'),
            reverse('admin_badge_create'),
            reverse('admin_badge_update', args=[self.insignia.pk]),
        ]
        
        for url in get_urls:
            # Anónimo
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302) # Redirige al login
            
            # Estudiante
            self.client.login(username='estudiante', password='password123')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 403) # Prohibido
            self.client.logout()
            
            # Administrador
            self.client.login(username='admin', password='password123')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.client.logout()

        # Probar vista de eliminación (solo POST)
        delete_url = reverse('admin_badge_delete', args=[self.insignia.pk])
        
        # Estudiante POST
        self.client.login(username='estudiante', password='password123')
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 403)
        self.client.logout()
        
        # Administrador POST (redirige tras éxito)
        self.client.login(username='admin', password='password123')
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)

    def test_list_view(self):
        """Verificar que el listado muestra las insignias."""
        self.client.login(username='admin', password='password123')
        response = self.client.get(reverse('admin_badge_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Prueba')

    def test_create_view(self):
        """Verificar creación de insignia."""
        self.client.login(username='admin', password='password123')
        data = {
            'nombre': 'Nueva Insignia',
            'descripcion': 'Nueva Desc',
            'icono_clase': 'fas fa-star',
            'tipo_regla': 'DOMINIO',
            'valor_requerido': 10
        }
        response = self.client.post(reverse('admin_badge_create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Insignia.objects.filter(nombre='Nueva Insignia').exists())

    def test_update_view(self):
        """Verificar actualización de insignia."""
        self.client.login(username='admin', password='password123')
        data = {
            'nombre': 'Nombre Editado',
            'descripcion': 'Desc Editada',
            'icono_clase': 'fas fa-edit',
            'tipo_regla': 'PROGRESION',
            'valor_requerido': 20
        }
        response = self.client.post(reverse('admin_badge_update', args=[self.insignia.pk]), data)
        self.assertEqual(response.status_code, 302)
        self.insignia.refresh_from_db()
        self.assertEqual(self.insignia.nombre, 'Nombre Editado')

    def test_delete_view(self):
        """Verificar eliminación de insignia."""
        self.client.login(username='admin', password='password123')
        response = self.client.post(reverse('admin_badge_delete', args=[self.insignia.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Insignia.objects.filter(pk=self.insignia.pk).exists())
