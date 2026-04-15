from django.db import models
from django.contrib.auth.models import User
from AppTutoria.models import Tema

# Create your models here.

class ExamenDiagnostico(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    tiempo_limite = models.IntegerField(help_text="Tiempo límite en minutos", default=45)

    def __str__(self):
        return self.nombre

class Examen(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE, related_name='examenes')
    cantidad_preguntas = models.IntegerField()
    tiempo_limite = models.IntegerField(help_text="Tiempo límite en minutos")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Pregunta(models.Model):
    TIPO_CHOICES = [
        ('OPCION_MULTIPLE', 'Opción Múltiple'),
        ('TEXTO_CORTO', 'Respuesta Corta'),
    ]
    
    DIFICULTAD_CHOICES = [
        ('Básico', 'Básico'),
        ('Intermedio', 'Intermedio'),
        ('Avanzado', 'Avanzado'),
    ]

    examen = models.ForeignKey(ExamenDiagnostico, on_delete=models.CASCADE, related_name='preguntas', null=True, blank=True)
    examen_tema = models.ForeignKey(Examen, on_delete=models.SET_NULL, null=True, blank=True, related_name='preguntas')
    texto = models.TextField()
    imagen = models.ImageField(upload_to='preguntas_imagenes/', blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='OPCION_MULTIPLE')
    tema = models.ForeignKey(Tema, on_delete=models.SET_NULL, null=True, related_name='preguntas_diagnostico')
    dificultad = models.CharField(max_length=20, choices=DIFICULTAD_CHOICES, default='Básico')

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

class Ejercicio(models.Model):
    DIFICULTAD_CHOICES = [
        ('Básico', 'Básico'),
        ('Intermedio', 'Intermedio'),
        ('Avanzado', 'Avanzado'),
    ]

    tema = models.ForeignKey(Tema, on_delete=models.CASCADE, related_name='ejercicios')
    texto = models.TextField()
    imagen = models.ImageField(upload_to='ejercicios_imagenes/', blank=True, null=True)
    dificultad = models.CharField(max_length=20, choices=DIFICULTAD_CHOICES, default='Básico')
    explicacion_tecnica = models.TextField(help_text="Explicación teórica general del ejercicio", blank=True, null=True)
    es_activo = models.BooleanField(default=True, help_text="Indica si el ejercicio está disponible para práctica")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tema.nombre} - {self.dificultad}: {self.texto[:50]}..."

class OpcionEjercicio(models.Model):
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE, related_name='opciones')
    texto = models.CharField(max_length=200)
    es_correcta = models.BooleanField(default=False)
    retroalimentacion = models.TextField(help_text="Mensaje que se muestra al estudiante tras elegir esta opción", blank=True, null=True)

    def __str__(self):
        return self.texto

class ResultadoEjercicio(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resultados_ejercicios')
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    es_correcto = models.BooleanField()
    fecha_resolucion = models.DateTimeField(auto_now_add=True)
    tiempo_empleado = models.IntegerField(help_text="Tiempo en segundos")
    feedback_mostrado = models.TextField()

    def __str__(self):
        estado = "Correcto" if self.es_correcto else "Incorrecto"
        return f"{self.usuario.username} - {self.ejercicio.id}: {estado}"
