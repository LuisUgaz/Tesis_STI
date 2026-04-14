from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from AppGestionUsuario.models import Profile

class AdminUserManagementTests(TestCase):
    def setUp(self):
        # Crear un Administrador
        self.admin_user = User.objects.create_user(username='admin_test', password='password123')
        self.admin_profile = Profile.objects.create(user=self.admin_user, rol='Administrador', nombres='Admin', apellidos='Test')
        
        # Crear un Estudiante
        self.student_user = User.objects.create_user(username='student_test', password='password123')
        self.student_profile = Profile.objects.create(user=self.student_user, rol='Estudiante', nombres='Student', apellidos='Test')
        
        # URLs (por definir en la implementación)
        self.list_url = reverse('admin_user_list')

    def test_access_restricted_to_admin(self):
        """Prueba que solo los administradores puedan acceder al listado."""
        # Intento como estudiante
        self.client.login(username='student_test', password='password123')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 403) # O redirección, según spec (Error 403)
        
        # Intento como administrador
        self.client.login(username='admin_test', password='password123')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_create_user_success(self):
        """Prueba la creación de un nuevo usuario por el admin."""
        self.client.login(username='admin_test', password='password123')
        create_url = reverse('admin_user_create')
        data = {
            'username': 'new_docente',
            'email': 'docente@test.com',
            'nombres': 'Docente',
            'apellidos': 'Nuevo',
            'rol': 'Docente',
            'is_active': True,
            'password_temporal': 'Temp123!'
        }
        response = self.client.post(create_url, data)
        self.assertEqual(response.status_code, 302)
        
        # Verificar en BD
        user = User.objects.get(username='new_docente')
        self.assertEqual(user.email, 'docente@test.com')
        self.assertEqual(user.profile.rol, 'Docente')
        self.assertTrue(user.check_password('Temp123!'))

    def test_update_user_success(self):
        """Prueba la edición de un usuario existente."""
        self.client.login(username='admin_test', password='password123')
        update_url = reverse('admin_user_update', kwargs={'pk': self.student_user.pk})
        data = {
            'username': 'student_test_mod',
            'email': 'student_mod@test.com',
            'nombres': 'Student',
            'apellidos': 'Modificado',
            'rol': 'Estudiante',
            'grado': '3',
            'seccion': 'B',
            'is_active': True
        }
        response = self.client.post(update_url, data)
        self.assertEqual(response.status_code, 302)
        
        # Verificar cambios
        self.student_user.refresh_from_db()
        self.assertEqual(self.student_user.username, 'student_test_mod')
        self.assertEqual(self.student_user.profile.apellidos, 'Modificado')
        self.assertEqual(self.student_user.profile.grado, '3')

    def test_toggle_user_status_ajax(self):
        """Prueba el cambio de estado (is_active) vía AJAX."""
        self.client.login(username='admin_test', password='password123')
        toggle_url = reverse('admin_user_toggle_status', kwargs={'pk': self.student_user.pk})
        
        # Desactivar
        response = self.client.post(toggle_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.student_user.refresh_from_db()
        self.assertFalse(self.student_user.is_active)
        self.assertEqual(response.json()['status'], 'inactive')
        
        # Activar de nuevo
        response = self.client.post(toggle_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.student_user.refresh_from_db()
        self.assertTrue(self.student_user.is_active)
        self.assertEqual(response.json()['status'], 'active')
