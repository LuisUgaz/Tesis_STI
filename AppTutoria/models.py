from django.db import models

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

class VideoTema(models.Model):
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE, related_name='videos')
    titulo = models.CharField(max_length=200)
    archivo_video = models.FileField(upload_to='videos_temas/', help_text="Archivo de video (MP4 preferible)")
    miniatura = models.ImageField(upload_to='videos_thumbnails/', help_text="Imagen de previsualización", blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True, help_text="Descripción breve del video")
    duracion = models.CharField(max_length=20, help_text="Ej: 5:30 min", blank=True, null=True)
    orden = models.PositiveIntegerField(default=1, help_text="Orden de visualización")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['orden', 'fecha_creacion']

    def __str__(self):
        return f"{self.titulo} ({self.tema.nombre})"
