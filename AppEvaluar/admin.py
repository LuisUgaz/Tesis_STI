from django.contrib import admin
from .models import ExamenDiagnostico, Pregunta, Opcion, RespuestaUsuario, ResultadoDiagnostico

class OpcionInline(admin.TabularInline):
    model = Opcion
    extra = 3

class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('texto', 'examen', 'tipo', 'categoria')
    list_filter = ('examen', 'tipo', 'categoria')
    inlines = [OpcionInline]

class PreguntaInline(admin.StackedInline):
    model = Pregunta
    extra = 1

class ExamenDiagnosticoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tiempo_limite', 'fecha_creacion')
    inlines = [PreguntaInline]

class RespuestaUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'pregunta', 'fecha_respuesta')
    list_filter = ('usuario', 'pregunta')
    readonly_fields = ('fecha_respuesta',)

class ResultadoDiagnosticoAdmin(admin.ModelAdmin):
    list_display = ('estudiante', 'examen', 'puntaje', 'fecha_realizacion')
    list_filter = ('examen', 'fecha_realizacion')
    readonly_fields = ('fecha_realizacion',)

admin.site.register(ExamenDiagnostico, ExamenDiagnosticoAdmin)
admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(RespuestaUsuario, RespuestaUsuarioAdmin)
admin.site.register(ResultadoDiagnostico, ResultadoDiagnosticoAdmin)
