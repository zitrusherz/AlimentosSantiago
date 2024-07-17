# gestion_pedidos/forms.py

from django import forms
from .models import Pedido, DetallePedido, Menu

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['cliente', 'fecha', 'platos']

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente', 'fecha_hora_entrega', 'repartidor']

class DetallePedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = ['plato', 'cantidad']

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [
        ('cliente', 'Cliente'),
        ('proveedor', 'Proveedor'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, label="Rol")

    class Meta:
        model = User
        fields = ("username", "role", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data["role"]
        if commit:
            user.save()
        return user
