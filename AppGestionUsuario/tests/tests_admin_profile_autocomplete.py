from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from AppGestionUsuario.models import Profile

class AdminProfileAutocompleteTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Crear un administrador
        self.admin_user = User.objects.create_superuser(
            username='admin_test',
            email='admin@test.com',
            password='password123'
        )
        # Crear un usuario con datos extendidos (usando setattr para degree y section)
        self.user_without_profile = User.objects.create(
            username='user_no_profile',
            first_name='Juan',
            last_name='Perez'
        )
        setattr(self.user_without_profile, 'degree', '3ro')
        setattr(self.user_without_profile, 'section', 'B')
        self.user_without_profile.save()

        # Crear un usuario con perfil
        self.user_with_profile = User.objects.create(
            username='user_with_profile',
            first_name='Maria',
            last_name='Gomez'
        )
        self.profile = Profile.objects.create(
            user=self.user_with_profile,
            nombres='Maria',
            apellidos='Gomez',
            rol='Estudiante'
        )
        
        self.client.login(username='admin_test', password='password123')

    def test_api_user_data_returns_correct_fields(self):
        """Validar que el endpoint devuelve los datos correctos para el autocompletado."""
        url = reverse('get_user_data', kwargs={'pk': self.user_without_profile.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['nombres'], 'Juan')
        self.assertEqual(data['apellidos'], 'Perez')
        self.assertEqual(data['grado'], '3ro')
        self.assertEqual(data['seccion'], 'B')

    def test_api_access_restricted_to_admin(self):
        """Validar que solo los administradores pueden acceder a los datos de usuario."""
        self.client.logout()
        
        # Estudiante intentando acceder
        student_user = User.objects.create_user(username='student', password='password123')
        Profile.objects.create(user=student_user, rol='Estudiante')
        self.client.login(username='student', password='password123')
        
        url = reverse('get_user_data', kwargs={'pk': self.user_without_profile.pk})
        response = self.client.get(url)
        # Debería dar PermissionDenied (403) por el AdminRequiredMixin
        self.assertEqual(response.status_code, 403)

    def test_admin_formfield_for_foreignkey_filtering(self):
        """Validar que el selector de usuarios en el admin filtra a los que ya tienen perfil."""
        from AppGestionUsuario.admin import ProfileAdmin
        from django.contrib.admin.sites import AdminSite
        
        model_admin = ProfileAdmin(Profile, AdminSite())
        
        # Simular una petición GET a la página de añadir
        from django.test import RequestFactory
        request = RequestFactory().get('/admin/AppGestionUsuario/profile/add/')
        request.user = self.admin_user
        # Resolver match simulado para el admin
        from django.urls import resolve
        request.resolver_match = resolve('/admin/AppGestionUsuario/profile/add/')

        db_field = Profile._meta.get_field('user')
        formfield = model_admin.formfield_for_foreignkey(db_field, request)
        
        # El queryset resultante no debe incluir al usuario que ya tiene perfil
        queryset_ids = list(formfield.queryset.values_list('id', flat=True))
        
        self.assertIn(self.user_without_profile.id, queryset_ids)
        self.assertNotIn(self.user_with_profile.id, queryset_ids)
        # El admin suele estar incluido porque es superuser y no tiene perfil
        self.assertIn(self.admin_user.id, queryset_ids)
