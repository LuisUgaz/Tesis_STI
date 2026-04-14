from django import forms
from django.contrib.auth.models import User
from .models import Profile
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
