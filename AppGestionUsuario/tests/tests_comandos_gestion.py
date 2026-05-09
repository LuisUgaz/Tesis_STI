from django.test import TestCase
from django.contrib.auth.models import User
from django.core.management import call_command
from AppGestionUsuario.models import Profile
import io

class AsignarEstudiantesCommandTest(TestCase):
    def setUp(self):
        # 1. Usuario sin perfil con degree y section (debe ser procesado)
        self.user_no_profile = User.objects.create_user(
            username='user_no_profile', 
            first_name='Juan', 
            last_name='Perez'
        )
        self.user_no_profile.degree = '2'
        self.user_no_profile.section = 'A'
        self.user_no_profile.save()
        
        # 2. Usuario con perfil de Estudiante pero sin grado/seccion (debe ser actualizado)
        self.user_update = User.objects.create_user(username='user_update')
        self.user_update.degree = '3'
        self.user_update.section = 'B'
        self.user_update.save()
        Profile.objects.create(
            user=self.user_update,
            nombres='Update',
            apellidos='Test',
            rol='Estudiante',
            grado='',
            seccion=''
        )
        
        # 3. Usuario que ya tiene perfil de Docente (no debe ser alterado)
        self.user_docente = User.objects.create_user(username='docente_test')
        self.user_docente.degree = 'Admin' # No debería migrarse a un Docente
        self.user_docente.save()
        Profile.objects.create(
            user=self.user_docente, 
            nombres='Admin', 
            apellidos='Tutor', 
            rol='Docente',
            grado='',
            seccion=''
        )

    def test_command_creates_and_updates_profiles(self):
        """Verifica que el comando crea y actualiza perfiles migrando grado y sección."""
        out = io.StringIO()
        call_command('asignar_estudiantes', stdout=out)
        
        # Verificar creación con grado y seccion
        profile1 = Profile.objects.get(user=self.user_no_profile)
        self.assertEqual(profile1.grado, '2')
        self.assertEqual(profile1.seccion, 'A')
        
        # Verificar actualización de perfil existente
        profile_upd = Profile.objects.get(user=self.user_update)
        self.assertEqual(profile_upd.grado, '3')
        self.assertEqual(profile_upd.seccion, 'B')
        
        # Verificar que el docente no fue alterado en su grado/sección
        profile_docente = Profile.objects.get(user=self.user_docente)
        self.assertEqual(profile_docente.rol, 'Docente')
        self.assertEqual(profile_docente.grado, '') # No se migra a Docentes
        
        # Verificar salida
        self.assertIn("Proceso completado", out.getvalue())

    def test_original_user_data_is_preserved(self):
        """Confirma que la tabla auth_user no pierde registros ni datos."""
        original_count = User.objects.count()
        call_command('asignar_estudiantes', stdout=io.StringIO())
        
        self.assertEqual(User.objects.count(), original_count)
        user = User.objects.get(username='user_no_profile')
        self.assertEqual(user.first_name, 'Juan')
