from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from gestion_pedidos.models import Cliente, Proveedor

ROLE_CHOICES = [
    ('cliente', 'Cliente'),
    ('proveedor', 'Proveedor'),
]

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if '@elcomilon.com' in email or 'zitrusherz' in email:
            raise forms.ValidationError("No puedes registrarte con este dominio.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data['email']
        role = self.cleaned_data['role']
        if commit:
            user.save()
            if role == 'cliente':
                Cliente.objects.create(usuario=user, nombre=user.username, email=email)
            elif role == 'proveedor':
                Proveedor.objects.create(usuario=user, nombre=user.username, contacto='', telefono='')
        return user
