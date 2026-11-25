from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistroForm(UserCreationForm):
    # Campo extra respecto al formulario de Django: el correo, obligatorio
    email = forms.EmailField(required=True, label='Correo electrónico')

    class Meta:
        model = User
        fields = ('username', 'email')  # las contraseñas ya las trae UserCreationForm

    # Validación propia: no permitir dos usuarios con el mismo correo
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Ya existe un usuario con este correo.')
        return email