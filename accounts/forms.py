# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from gestion_pedidos.models import Cliente

ROLE_CHOICES = [
    ('cliente', 'Cliente'),
    ('proveedor', 'Proveedor'),
]

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'role')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if '@elcomilon.com' in email or 'zitrusherz' in email:
            raise forms.ValidationError("No puedes registrarte con este dominio.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        if self.cleaned_data['role'] == 'cliente':
            Cliente.objects.create(usuario=user, nombre=user.username, email=user.email)
        return user
