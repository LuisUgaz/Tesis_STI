from django.contrib import admin
from .models import (
    ExamenDiagnostico, Pregunta, Opcion, RespuestaUsuario, 
    ResultadoDiagnostico, RecomendacionEstudiante,
    Ejercicio, OpcionEjercicio, ResultadoEjercicio
)

# --- Examen Diagnóstico ---

class OpcionInline(admin.TabularInline):
    model = Opcion
    fields = ('texto', 'es_correcta', 'retroalimentacion')
    extra = 3

class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('texto', 'examen', 'tipo', 'tema', 'dificultad')
    list_filter = ('examen', 'tipo', 'tema', 'dificultad')
    inlines = [OpcionInline]
    fieldsets = (
        (None, {
            'fields': ('examen', 'texto', 'imagen', 'tipo', 'explicacion_tecnica')
        }),
        ('Clasificación Académica', {
            'fields': ('tema', 'dificultad'),
            'description': 'Especifique el tema y nivel para la selección adaptativa.'
        }),
    )

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
    list_display = ('estudiante', 'dificultad_actual', 'tema_recomendado', 'examen', 'puntaje', 'fecha_realizacion')
    list_filter = ('examen', 'fecha_realizacion')
    readonly_fields = ('fecha_realizacion',)

    def dificultad_actual(self, obj):
        return obj.estudiante.profile.nivel_dificultad_actual if hasattr(obj.estudiante, 'profile') else '-'
    dificultad_actual.short_description = 'Dificultad Actual'
    dificultad_actual.admin_order_field = 'estudiante__profile__nivel_dificultad_actual'

    def tema_recomendado(self, obj):
        rec = RecomendacionEstudiante.objects.filter(usuario=obj.estudiante).first()
        return rec.tema if rec else '-'
    tema_recomendado.short_description = 'Tema Recomendado'
    tema_recomendado.admin_order_field = 'estudiante__recomendaciones__tema'

# --- Prácticas Personalizadas (HU14) ---

class OpcionEjercicioInline(admin.TabularInline):
    model = OpcionEjercicio
    extra = 4

@admin.register(Ejercicio)
class EjercicioAdmin(admin.ModelAdmin):
    list_display = ('texto_corto', 'tema', 'dificultad', 'es_interactiva', 'fecha_creacion')
    list_filter = ('tema', 'dificultad', 'es_interactiva', 'fecha_creacion')
    search_fields = ('texto',)
    inlines = [OpcionEjercicioInline]
    fieldsets = (
        (None, {
            'fields': ('tema', 'texto', 'imagen', 'dificultad', 'explicacion_tecnica', 'es_activo')
        }),
        ('Interactividad (HU45)', {
            'fields': ('es_interactiva', 'meta_geometria'),
            'description': 'Configure el plano interactivo JSXGraph y los objetivos geométricos.'
        }),
    )

    def texto_corto(self, obj):
        return obj.texto[:75] + "..." if len(obj.texto) > 75 else obj.texto
    texto_corto.short_description = "Pregunta"

@admin.register(ResultadoEjercicio)
class ResultadoEjercicioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'dificultad_actual', 'tema_recomendado', 'ejercicio_id', 'es_correcto', 'tiempo_empleado', 'fecha_resolucion')
    list_filter = ('es_correcto', 'fecha_resolucion', 'ejercicio__tema')
    readonly_fields = ('fecha_resolucion',)

    def ejercicio_id(self, obj):
        return f"Ejercicio #{obj.ejercicio.id}"

    def dificultad_actual(self, obj):
        return obj.usuario.profile.nivel_dificultad_actual if hasattr(obj.usuario, 'profile') else '-'
    dificultad_actual.short_description = 'Dificultad Actual'
    dificultad_actual.admin_order_field = 'usuario__profile__nivel_dificultad_actual'

    def tema_recomendado(self, obj):
        rec = RecomendacionEstudiante.objects.filter(usuario=obj.usuario).first()
        return rec.tema if rec else '-'
    tema_recomendado.short_description = 'Tema Recomendado'
    tema_recomendado.admin_order_field = 'usuario__recomendaciones__tema'

@admin.register(RecomendacionEstudiante)
class RecomendacionEstudianteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tema', 'metrica_desempeno', 'fecha_generacion')
    list_filter = ('tema', 'fecha_generacion')

admin.site.register(ExamenDiagnostico, ExamenDiagnosticoAdmin)
admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(RespuestaUsuario, RespuestaUsuarioAdmin)
admin.site.register(ResultadoDiagnostico, ResultadoDiagnosticoAdmin)
