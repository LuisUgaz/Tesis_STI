from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm
from django.contrib import messages

class RegisterView(FormView):
    template_name = 'AppGestionUsuario/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login') # Supongamos que hay una URL de login

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Registro exitoso. Ahora puedes iniciar sesión.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error en el registro. Por favor, verifica los campos.")
        return super().form_invalid(form)
