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

class MetricasEstudiante(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='metricas')
    precision_general = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, help_text="Porcentaje de aciertos global")
    rendimiento_academico = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, help_text="Promedio de puntajes")
    tiempo_respuesta_promedio = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, help_text="Tiempo medio de resoluciÃ³n en segundos")
    dominio_por_tema = models.JSONField(default=dict, help_text="Nivel de acierto por categorÃ­a de geometrÃ­a")
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"MÃ©tricas de {self.usuario.username}"
