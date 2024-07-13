from django.db import models
from django.utils import timezone



class Proveedor(models.Model):
    nombre = models.CharField(max_length=200)
    contacto = models.CharField(max_length=200)
    telefono = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Plato(models.Model):
    nombre = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - {self.precio}€"

class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return self.nombre

class Repartidor(models.Model):
    nombre = models.CharField(max_length=200)
    telefono = models.CharField(max_length=50)
    rutas = models.TextField()

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    ESTADO_PEDIDO = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('en_camino', 'En Camino'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    platos = models.ManyToManyField(Plato, through='DetallePedido')
    fecha_hora_pedido = models.DateTimeField(default=timezone.now)  # Aquí se define el valor predeterminado
    fecha_hora_entrega = models.DateTimeField()
    estado = models.CharField(max_length=100, choices=ESTADO_PEDIDO, default='pendiente')
    repartidor = models.ForeignKey(Repartidor, on_delete=models.SET_NULL, null=True, blank=True)

    def calcular_total(self):
        return sum(detalle.subtotal for detalle in self.detallepedido_set.all())

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.nombre}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.plato.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.plato.nombre}"
class Menu(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateField()
    platos = models.ManyToManyField(Plato)

    def __str__(self):
        return f"Menu {self.fecha} - {self.cliente.nombre}"