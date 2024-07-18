

from django import forms
from .models import Pedido, DetallePedido, Menu

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cliente', 'fecha_hora_entrega', 'estado', 'repartidor']  # Incluye cliente


class DetallePedidoForm(forms.ModelForm):
    class Meta:
        model = DetallePedido
        fields = ['pedido', 'plato', 'cantidad']

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['cliente', 'fecha', 'platos']