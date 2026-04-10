from django.contrib import admin
from .models import Tema, ContenidoTema, VideoTema

@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug')
    prepopulated_fields = {"slug": ("nombre",)}

@admin.register(ContenidoTema)
class ContenidoTemaAdmin(admin.ModelAdmin):
    list_display = ('tema', 'fecha_actualizacion')

@admin.register(VideoTema)
class VideoTemaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tema', 'orden', 'duracion')
    list_filter = ('tema',)
    search_fields = ('titulo', 'descripcion')
