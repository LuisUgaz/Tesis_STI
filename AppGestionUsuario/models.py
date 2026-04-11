from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    ROLE_CHOICES = [
        ('Estudiante', 'Estudiante'),
        ('Docente', 'Docente'),
        ('Administrador', 'Administrador'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    grado = models.CharField(max_length=10, blank=True, null=True)
    seccion = models.CharField(max_length=10, blank=True, null=True)
    rol = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Estudiante')
    
    DIFICULTAD_CHOICES = [
        ('Básico', 'Básico'),
        ('Intermedio', 'Intermedio'),
        ('Avanzado', 'Avanzado'),
    ]
    nivel_dificultad_actual = models.CharField(
        max_length=20, 
        choices=DIFICULTAD_CHOICES, 
        default='Básico',
        help_text="Nivel de dificultad asignado automáticamente por el sistema"
    )

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.user.username})"
