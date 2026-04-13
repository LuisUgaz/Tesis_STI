from django import forms
from .models import VideoTema
from .utils import extraer_youtube_id, generar_youtube_thumbnail

class VideoTemaForm(forms.ModelForm):
    class Meta:
        model = VideoTema
        fields = ['tema', 'titulo', 'descripcion', 'url_video', 'duracion', 'orden']
        widgets = {
            'tema': forms.Select(attrs={'class': 'form-select', 'style': 'border-radius: 10px;'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del video', 'style': 'border-radius: 10px;'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción breve...', 'style': 'border-radius: 10px;'}),
            'url_video': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.youtube.com/watch?v=...', 'style': 'border-radius: 10px;'}),
            'duracion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 5:30 min', 'style': 'border-radius: 10px;'}),
            'orden': forms.NumberInput(attrs={'class': 'form-control', 'style': 'border-radius: 10px;'}),
        }

    def clean_url_video(self):
        url = self.cleaned_data.get('url_video')
        if url:
            video_id = extraer_youtube_id(url)
            if not video_id:
                raise forms.ValidationError("Debe ingresar una URL válida de YouTube.")
        return url

    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.url_video:
            instance.url_miniatura = generar_youtube_thumbnail(instance.url_video)
        if commit:
            instance.save()
        return instance
