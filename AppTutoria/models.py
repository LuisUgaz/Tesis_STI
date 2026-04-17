from django.db import models
from django.contrib.auth.models import User

class Tema(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class ContenidoTema(models.Model):
    tema = models.OneToOneField(Tema, on_delete=models.CASCADE, related_name='contenido')
    cuerpo_html = models.TextField(help_text="Contenido educativo en formato HTML")
    material_pdf = models.FileField(upload_to='material_temas/', blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Contenido de {self.tema.nombre}"

class ImagenContenido(models.Model):
    contenido = models.ForeignKey(ContenidoTema, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='teoria_imagenes/')
    orden = models.PositiveIntegerField(default=1, help_text="Orden de aparición en el carrusel")
    descripcion_alt = models.CharField(max_length=200, blank=True, null=True, help_text="Descripción para accesibilidad")

    class Meta:
        verbose_name = "Imagen de Teoría"
        verbose_name_plural = "Imágenes de Teoría"
        ordering = ['orden']

    def __str__(self):
        return f"Imagen {self.orden} de {self.contenido.tema.nombre}"

class VideoTema(models.Model):
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE, related_name='videos')
    titulo = models.CharField(max_length=200)
    # Soporte híbrido: Archivo local o URL externa
    archivo_video = models.FileField(upload_to='videos_temas/', help_text="Archivo de video (MP4 preferible)", blank=True, null=True)
    url_video = models.URLField(max_length=500, help_text="URL de video externo (YouTube)", blank=True, null=True)
    
    # Miniatura: Imagen local o URL externa
    miniatura = models.ImageField(upload_to='videos_thumbnails/', help_text="Imagen de previsualización local", blank=True, null=True)
    url_miniatura = models.URLField(max_length=500, help_text="URL de miniatura externa (YouTube)", blank=True, null=True)
    
    descripcion = models.TextField(blank=True, null=True, help_text="Descripción breve del video")
    duracion = models.CharField(max_length=20, help_text="Ej: 5:30 min", blank=True, null=True)
    orden = models.PositiveIntegerField(default=1, help_text="Orden de visualización")
    es_activo = models.BooleanField(default=True, help_text="Indica si el video está activo en el catálogo")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['orden', 'fecha_creacion']

    def __str__(self):
        return f"{self.titulo} ({self.tema.nombre})"

class VisualizacionVideo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visualizaciones_videos')
    video = models.ForeignKey(VideoTema, on_delete=models.CASCADE, related_name='vistas')
    contador = models.PositiveIntegerField(default=0)
    fecha_primera_vista = models.DateTimeField(auto_now_add=True)
    fecha_ultima_vista = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('usuario', 'video')
        verbose_name = "Visualización de Video"
        verbose_name_plural = "Visualizaciones de Videos"

    def __str__(self):
        return f"{self.usuario.username} vio {self.video.titulo} ({self.contador} veces)"

class ProgresoEstudiante(models.Model):
    TIPO_ACTIVIDAD_CHOICES = [
        ('Ejercicio', 'Ejercicio'),
        ('Video', 'Video'),
        ('Teoría', 'Teoría'),
        ('Examen', 'Examen'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progresos')
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE, related_name='progresos_estudiantes')
    tipo_actividad = models.CharField(max_length=20, choices=TIPO_ACTIVIDAD_CHOICES)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    grado = models.CharField(max_length=10)
    seccion = models.CharField(max_length=10)
    referencia_id = models.PositiveIntegerField(null=True, blank=True, help_text="ID de la actividad específica (ejercicio, video, etc.)")
    porcentaje_completado = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, help_text="Porcentaje de avance en la actividad (0-100)")

    class Meta:
        verbose_name = "Progreso del Estudiante"
        verbose_name_plural = "Progresos de los Estudiantes"
        ordering = ['-fecha_registro']

    def __str__(self):
        return f"{self.usuario.username} - {self.tema.nombre} - {self.tipo_actividad}"

    def get_resultado_detalle(self):
        """
        Retorna el resultado detallado dependiendo del tipo de actividad.
        """
        from AppEvaluar.models import ResultadoEjercicio, ResultadoDiagnostico
        
        if self.tipo_actividad == 'Ejercicio' and self.referencia_id:
            res = ResultadoEjercicio.objects.filter(usuario=self.usuario, ejercicio_id=self.referencia_id).order_by('-fecha_resolucion').first()
            if res:
                return "Correcto" if res.es_correcto else "Incorrecto"
        
        elif self.tipo_actividad == 'Examen' and self.referencia_id:
            res = ResultadoDiagnostico.objects.filter(estudiante=self.usuario, examen_id=self.referencia_id).first()
            if res:
                return f"Puntaje: {res.puntaje}%"
        
        elif self.tipo_actividad == 'Video':
            return "Visualizado"
            
        elif self.tipo_actividad == 'Teoría':
            return "Completado"
            
        return "-"
