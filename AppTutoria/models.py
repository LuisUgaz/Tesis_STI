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
