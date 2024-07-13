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
