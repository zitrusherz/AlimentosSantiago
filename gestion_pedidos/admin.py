from django.contrib import admin

# Register your models here.
from .models import Proveedor, Plato, Cliente, Pedido, Repartidor

admin.site.register(Proveedor)
admin.site.register(Plato)
admin.site.register(Cliente)
admin.site.register(Pedido)
admin.site.register(Repartidor)