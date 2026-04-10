from django.contrib import admin
from .models import (
    ExamenDiagnostico, Pregunta, Opcion, RespuestaUsuario, 
    ResultadoDiagnostico, RecomendacionEstudiante,
    Ejercicio, OpcionEjercicio, ResultadoEjercicio
)

# --- Examen Diagnóstico ---

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

# --- Prácticas Personalizadas (HU14) ---

class OpcionEjercicioInline(admin.TabularInline):
    model = OpcionEjercicio
    extra = 4

@admin.register(Ejercicio)
class EjercicioAdmin(admin.ModelAdmin):
    list_display = ('texto_corto', 'tema', 'dificultad', 'fecha_creacion')
    list_filter = ('tema', 'dificultad', 'fecha_creacion')
    search_fields = ('texto',)
    inlines = [OpcionEjercicioInline]

    def texto_corto(self, obj):
        return obj.texto[:75] + "..." if len(obj.texto) > 75 else obj.texto
    texto_corto.short_description = "Pregunta"

@admin.register(ResultadoEjercicio)
class ResultadoEjercicioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'ejercicio_id', 'es_correcto', 'tiempo_empleado', 'fecha_resolucion')
    list_filter = ('es_correcto', 'fecha_resolucion', 'ejercicio__tema')
    readonly_fields = ('fecha_resolucion',)

    def ejercicio_id(self, obj):
        return f"Ejercicio #{obj.ejercicio.id}"

@admin.register(RecomendacionEstudiante)
class RecomendacionEstudianteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tema', 'metrica_desempeno', 'fecha_generacion')
    list_filter = ('tema', 'fecha_generacion')

admin.site.register(ExamenDiagnostico, ExamenDiagnosticoAdmin)
admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(RespuestaUsuario, RespuestaUsuarioAdmin)
admin.site.register(ResultadoDiagnostico, ResultadoDiagnosticoAdmin)
