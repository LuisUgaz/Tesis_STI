from django.contrib import admin
from .models import Tema, ContenidoTema, ImagenContenido, VideoTema, VisualizacionVideo

class ImagenContenidoInline(admin.TabularInline):
    model = ImagenContenido
    extra = 5  # Muestra 5 espacios vacíos para subir imágenes rápidamente
    fields = ('imagen', 'orden', 'descripcion_alt')

@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug')
    prepopulated_fields = {"slug": ("nombre",)}

@admin.register(ContenidoTema)
class ContenidoTemaAdmin(admin.ModelAdmin):
    list_display = ('tema', 'fecha_actualizacion')
    inlines = [ImagenContenidoInline]

@admin.register(VideoTema)
class VideoTemaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tema', 'orden', 'duracion')
    list_filter = ('tema',)
    search_fields = ('titulo', 'descripcion')

@admin.register(VisualizacionVideo)
class VisualizacionVideoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'get_grado', 'get_seccion', 'video', 'contador', 'fecha_ultima_vista')
    list_filter = ('usuario__profile__grado', 'usuario__profile__seccion', 'video__tema')
    search_fields = ('usuario__username', 'video__titulo')

    def get_grado(self, obj):
        return obj.usuario.profile.grado if hasattr(obj.usuario, 'profile') else "-"
    get_grado.short_description = 'Grado'

    def get_seccion(self, obj):
        return obj.usuario.profile.seccion if hasattr(obj.usuario, 'profile') else "-"
    get_seccion.short_description = 'Sección'
