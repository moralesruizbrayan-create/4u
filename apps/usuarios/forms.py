# apps/usuarios/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm

class RegistroUsuarioForm(UserCreationForm):
    # Aquí podrías agregar campos extra como email si quisieras
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)