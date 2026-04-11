from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nombres', 'apellidos', 'grado', 'seccion', 'rol', 'nivel_dificultad_actual')
    list_filter = ('rol', 'grado', 'seccion', 'nivel_dificultad_actual')
    search_fields = ('user__username', 'nombres', 'apellidos')
    fieldsets = (
        ('Información Personal', {
            'fields': ('user', 'nombres', 'apellidos')
        }),
        ('Información Académica', {
            'fields': ('grado', 'seccion', 'rol')
        }),
        ('Aprendizaje Adaptativo', {
            'fields': ('nivel_dificultad_actual',),
            'description': 'Configuración del nivel de dificultad para el sistema tutor inteligente.'
        }),
    )
