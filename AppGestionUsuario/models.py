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
    puntos_acumulados = models.PositiveIntegerField(
        default=0, 
        help_text="Puntos de experiencia acumulados por el estudiante"
    )
    nivel_estudiante = models.PositiveIntegerField(
        default=1,
        help_text="Nivel de progresión del estudiante basado en XP"
    )

    def __str__(self):
        return f"{self.nombres} {self.apellidos} ({self.user.username})"

    def save(self, *args, **kwargs):
        # Normalizar sección a mayúsculas si existe
        if self.seccion:
            self.seccion = self.seccion.upper()
        super(Profile, self).save(*args, **kwargs)

class Insignia(models.Model):
    RULE_TYPES = [
        ('HITOS', 'Hitos de Actividad'),
        ('DOMINIO', 'Dominio de Tema'),
        ('CONSTANCIA', 'Constancia/Racha'),
        ('PROGRESION', 'Progresión de Nivel'),
    ]
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    icono_clase = models.CharField(max_length=50, help_text="Clase de FontAwesome o icono visual")
    tipo_regla = models.CharField(max_length=20, choices=RULE_TYPES)
    valor_requerido = models.IntegerField(default=1, help_text="Valor numérico para cumplir la regla (ej: 100 puntos, 5 ejercicios)")

    def __str__(self):
        return self.nombre

class LogroEstudiante(models.Model):
    perfil = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='logros')
    insignia = models.ForeignKey(Insignia, on_delete=models.CASCADE)
    fecha_obtencion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('perfil', 'insignia')
        verbose_name_plural = "Logros de Estudiantes"

    def __str__(self):
        return f"{self.perfil.user.username} - {self.insignia.nombre}"

class MetricasEstudiante(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='metricas')
    precision_general = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, help_text="Porcentaje de aciertos global")
    rendimiento_academico = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, help_text="Promedio de puntajes")
    tiempo_respuesta_promedio = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, help_text="Tiempo medio de resoluciÃ³n en segundos")
    dominio_por_tema = models.JSONField(default=dict, help_text="Nivel de acierto por categorÃ­a de geometrÃ­a")
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"MÃ©tricas de {self.usuario.username}"

class ConfiguracionGlobal(models.Model):
    nombre_sistema = models.CharField(max_length=200, default="Tesis STI")
    email_contacto = models.EmailField(default="luisugaz63@gmail.com")
    texto_footer = models.TextField(default="© 2026 Tesis STI - Inteligencia en Geometría", blank=True, null=True)

    class Meta:
        verbose_name = "Configuración Global"
        verbose_name_plural = "Configuraciones Globales"

    def __str__(self):
        return f"Configuración Global - {self.nombre_sistema}"

    def save(self, *args, **kwargs):
        # Garantizar Singleton: si ya existe uno, actualizarlo
        if not self.pk and ConfiguracionGlobal.objects.exists():
            # Debería haber solo uno
            return
        return super(ConfiguracionGlobal, self).save(*args, **kwargs)

class PaginaEstatica(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    contenido_html = models.TextField(blank=True, null=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Página Estática"
        verbose_name_plural = "Páginas Estáticas"

    def __str__(self):
        return f"Página: {self.titulo}"
