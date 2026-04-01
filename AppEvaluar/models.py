from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ExamenDiagnostico(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    tiempo_limite = models.IntegerField(help_text="Tiempo límite en minutos", default=45)

    def __str__(self):
        return self.nombre

class Pregunta(models.Model):
    TIPO_CHOICES = [
        ('OPCION_MULTIPLE', 'Opción Múltiple'),
        ('TEXTO_CORTO', 'Respuesta Corta'),
    ]

    examen = models.ForeignKey(ExamenDiagnostico, on_delete=models.CASCADE, related_name='preguntas')
    texto = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='OPCION_MULTIPLE')
    categoria = models.CharField(max_length=100, help_text="Ej: Triángulos, Ángulos, etc.")

    def __str__(self):
        return self.texto

class Opcion(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='opciones')
    texto = models.CharField(max_length=200)
    es_correcta = models.BooleanField(default=False)

    def __str__(self):
        return self.texto

class RespuestaUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='respuestas_evaluacion')
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    opcion_seleccionada = models.ForeignKey(Opcion, on_delete=models.CASCADE, null=True, blank=True)
    respuesta_texto = models.TextField(null=True, blank=True)
    fecha_respuesta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Respuesta de {self.usuario.username} a {self.pregunta.id}"

class ResultadoDiagnostico(models.Model):
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resultados_diagnostico')
    examen = models.ForeignKey(ExamenDiagnostico, on_delete=models.CASCADE)
    puntaje = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_realizacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Resultado {self.estudiante.username} - {self.puntaje}%"

class RecomendacionEstudiante(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recomendaciones')
    tema = models.CharField(max_length=100)
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    metrica_desempeno = models.DecimalField(max_digits=5, decimal_places=2, help_text="Porcentaje de acierto en el tema")

    def __str__(self):
        return f"Recomendación para {self.usuario.username}: {self.tema}"
