from django import forms
from django.contrib.auth.models import User
from .models import Profile, ConfiguracionGlobal, PaginaEstatica, Insignia
from django.core.exceptions import ValidationError

class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150, label="Nombre de Usuario")
    email = forms.EmailField(label="Correo Electrónico")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")
    
    nombres = forms.CharField(max_length=100, label="Nombres")
    apellidos = forms.CharField(max_length=100, label="Apellidos")
    grado = forms.CharField(max_length=10, required=False, label="Grado")
    seccion = forms.CharField(max_length=10, required=False, label="Sección")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("El nombre de usuario ya existe.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("El correo electrónico ya está registrado.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Las contraseñas no coinciden.")

        # Validación de contraseña fuerte (mínimo 8 caracteres, números y símbolos)
        if password:
            if len(password) < 8:
                self.add_error('password', "La contraseña debe tener al menos 8 caracteres.")
            if not any(char.isdigit() for char in password):
                self.add_error('password', "La contraseña debe incluir al menos un número.")
            if not any(not char.isalnum() for char in password):
                self.add_error('password', "La contraseña debe incluir al menos un símbolo.")

        return cleaned_data

    def save(self):
        cleaned_data = self.cleaned_data
        user = User.objects.create_user(
            username=cleaned_data['username'],
            email=cleaned_data['email'],
            password=cleaned_data['password']
        )
        Profile.objects.create(
            user=user,
            nombres=cleaned_data['nombres'],
            apellidos=cleaned_data['apellidos'],
            grado=cleaned_data['grado'],
            seccion=cleaned_data['seccion'],
            rol='Estudiante'
        )
        return user

class ContactoForm(forms.Form):
    asunto = forms.CharField(max_length=200, label="Asunto")
    mensaje = forms.CharField(widget=forms.Textarea, label="Mensaje")
    tema_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    ejercicio_id = forms.IntegerField(required=False, widget=forms.HiddenInput())

class AdminUserForm(forms.ModelForm):
    nombres = forms.CharField(max_length=100, label="Nombres")
    apellidos = forms.CharField(max_length=100, label="Apellidos")
    rol = forms.ChoiceField(choices=Profile.ROLE_CHOICES, label="Rol")
    grado = forms.CharField(max_length=10, required=False, label="Grado (Estudiantes)")
    seccion = forms.CharField(max_length=10, required=False, label="Sección (Estudiantes)")
    password_temporal = forms.CharField(
        required=False, 
        widget=forms.PasswordInput(attrs={'placeholder': 'Opcional (si se deja vacío no se cambiará)'}),
        label="Password Temporal"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            try:
                profile = self.instance.profile
                self.fields['nombres'].initial = profile.nombres
                self.fields['apellidos'].initial = profile.apellidos
                self.fields['rol'].initial = profile.rol
                self.fields['grado'].initial = profile.grado
                self.fields['seccion'].initial = profile.seccion
            except Profile.DoesNotExist:
                pass

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError("El correo electrónico es obligatorio.")
        
        qs = User.objects.filter(email=email)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
            
        if qs.exists():
            raise ValidationError("Este correo electrónico ya está en uso por otro usuario.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password_temporal')
        if password:
            user.set_password(password)
        
        if commit:
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)
            profile.nombres = self.cleaned_data['nombres']
            profile.apellidos = self.cleaned_data['apellidos']
            profile.rol = self.cleaned_data['rol']
            profile.grado = self.cleaned_data['grado']
            profile.seccion = self.cleaned_data['seccion']
            profile.save()
        return user

class ConfiguracionGlobalForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionGlobal
        fields = ['nombre_sistema', 'email_contacto', 'texto_footer']
        widgets = {
            'nombre_sistema': forms.TextInput(attrs={'class': 'form-control'}),
            'email_contacto': forms.EmailInput(attrs={'class': 'form-control'}),
            'texto_footer': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class PaginaEstaticaForm(forms.ModelForm):
    class Meta:
        model = PaginaEstatica
        fields = ['titulo', 'slug', 'contenido_html']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'contenido_html': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }

class InsigniaForm(forms.ModelForm):
    class Meta:
        model = Insignia
        fields = ['nombre', 'descripcion', 'icono_clase', 'tipo_regla', 'valor_requerido']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Maestro de Triángulos'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe cómo se obtiene esta insignia...'}),
            'icono_clase': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: fas fa-medal'}),
            'tipo_regla': forms.Select(attrs={'class': 'form-select'}),
            'valor_requerido': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
        labels = {
            'nombre': 'Nombre de la Insignia',
            'descripcion': 'Descripción',
            'icono_clase': 'Clase de Icono (FontAwesome)',
            'tipo_regla': 'Tipo de Regla de Asignación',
            'valor_requerido': 'Valor Requerido (Hito)',
        }
