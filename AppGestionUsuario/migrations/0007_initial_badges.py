from django.db import migrations

def create_initial_badges(apps, schema_editor):
    Insignia = apps.get_model('AppGestionUsuario', 'Insignia')
    
    badges = [
        {
            'nombre': 'Primeros Pasos',
            'descripcion': 'Completaste tu primer ejercicio de práctica.',
            'icono_clase': 'fa-running',
            'tipo_regla': 'HITOS',
            'valor_requerido': 1
        },
        {
            'nombre': 'Maestro de Triángulos',
            'descripcion': 'Alcanzaste una precisión del 80% en el tema Triángulos.',
            'icono_clase': 'fa-shapes',
            'tipo_regla': 'DOMINIO',
            'valor_requerido': 80
        },
        {
            'nombre': 'Perseverante',
            'descripcion': 'Completaste actividades en 3 días diferentes.',
            'icono_clase': 'fa-calendar-check',
            'tipo_regla': 'CONSTANCIA',
            'valor_requerido': 3
        },
        {
            'nombre': 'Veterano (Nivel 5)',
            'descripcion': 'Alcanzaste el nivel 5 de experiencia.',
            'icono_clase': 'fa-medal',
            'tipo_regla': 'PROGRESION',
            'valor_requerido': 5
        }
    ]
    
    for badge_data in badges:
        Insignia.objects.get_or_create(nombre=badge_data['nombre'], defaults=badge_data)

def remove_initial_badges(apps, schema_editor):
    Insignia = apps.get_model('AppGestionUsuario', 'Insignia')
    Insignia.objects.filter(nombre__in=[
        'Primeros Pasos', 'Maestro de Triángulos', 'Perseverante', 'Veterano (Nivel 5)'
    ]).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('AppGestionUsuario', '0006_insignia_logroestudiante'),
    ]

    operations = [
        migrations.RunPython(create_initial_badges, remove_initial_badges),
    ]
