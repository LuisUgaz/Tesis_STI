from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
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

    class Media:
        js = ('AppGestionUsuario/js/admin_profile.js',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            # Si estamos editando un perfil existente, permitimos que el usuario actual aparezca en la lista
            # Si estamos creando uno nuevo, solo mostramos usuarios sin perfil
            profile_id = request.resolver_match.kwargs.get('object_id')
            if profile_id:
                # Caso edición: permitir al usuario actual + usuarios sin perfil
                profile = Profile.objects.get(pk=profile_id)
                kwargs["queryset"] = User.objects.filter(
                    models.Q(profile__isnull=True) | models.Q(pk=profile.user.pk)
                )
            else:
                # Caso creación: solo usuarios sin perfil
                kwargs["queryset"] = User.objects.filter(profile__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
