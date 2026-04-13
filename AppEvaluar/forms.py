from django import forms
from django.forms import inlineformset_factory
from .models import Ejercicio, OpcionEjercicio

class EjercicioForm(forms.ModelForm):
    class Meta:
        model = Ejercicio
        fields = ['texto', 'tema', 'dificultad', 'explicacion_tecnica', 'imagen']
        widgets = {
            'texto': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Escriba el enunciado del problema geométrico...'}),
            'tema': forms.Select(attrs={'class': 'form-select'}),
            'dificultad': forms.Select(attrs={'class': 'form-select'}),
            'explicacion_tecnica': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Explique la solución para el feedback inmediato...'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

OpcionEjercicioFormSet = inlineformset_factory(
    Ejercicio, 
    OpcionEjercicio,
    fields=['texto', 'es_correcta', 'retroalimentacion'],
    extra=5,
    min_num=5,
    max_num=5,
    can_delete=False,
    widgets={
        'texto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Texto de la opción'}),
        'es_correcta': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        'retroalimentacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Retroalimentación opcional'}),
    }
)
