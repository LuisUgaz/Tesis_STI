from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from AppGestionUsuario.models import Profile
from django.db import transaction

class Command(BaseCommand):
    help = 'Asigna o actualiza masivamente perfiles de Estudiante a usuarios, migrando grado y sección.'

    def handle(self, *args, **options):
        # Obtener todos los usuarios que no son superusuarios
        usuarios = User.objects.filter(is_superuser=False)
        total_a_procesar = usuarios.count()
        
        if total_a_procesar == 0:
            self.stdout.write(self.style.SUCCESS('No se encontraron usuarios para procesar.'))
            return

        self.stdout.write(f"Iniciando procesamiento de {total_a_procesar} usuarios...")
        
        creados = 0
        actualizados = 0
        errores = 0

        with transaction.atomic():
            for user in usuarios:
                try:
                    # Preparar datos básicos
                    nombres = user.first_name if user.first_name else user.username
                    apellidos = user.last_name if user.last_name else user.username
                    # Migrar campos degree y section
                    grado = getattr(user, 'degree', '')
                    seccion = getattr(user, 'section', '')
                    
                    # Buscar si ya tiene perfil
                    profile, created = Profile.objects.get_or_create(
                        user=user,
                        defaults={
                            'nombres': nombres,
                            'apellidos': apellidos,
                            'rol': 'Estudiante',
                            'grado': grado,
                            'seccion': seccion
                        }
                    )
                    
                    if created:
                        creados += 1
                    else:
                        # Si ya existía, actualizamos el grado y sección si están vacíos o han cambiado
                        # Solo actualizamos si el rol es Estudiante para no sobreescribir Docentes/Admins
                        if profile.rol == 'Estudiante':
                            profile.grado = grado
                            profile.seccion = seccion
                            profile.save()
                            actualizados += 1
                            
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error al procesar perfil para {user.username}: {e}"))
                    errores += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Proceso completado."))
        self.stdout.write(f"- Perfiles creados: {creados}")
        self.stdout.write(f"- Perfiles actualizados: {actualizados}")
        if errores > 0:
            self.stdout.write(self.style.ERROR(f"- Errores: {errores}"))
