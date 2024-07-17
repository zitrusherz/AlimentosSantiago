from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator

class Proveedor(models.Model):
    nombre = models.CharField(max_length=200)
    contacto = models.CharField(max_length=200)
    telefono = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Plato(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(default='Descripción no disponible')
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='platos')
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to='platos/', default='images/default.png')

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(0)])

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

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos')
    platos = models.ManyToManyField(Plato, through='DetallePedido')
    fecha_hora_pedido = models.DateTimeField(default=timezone.now)
    fecha_hora_entrega = models.DateTimeField()
    estado = models.CharField(max_length=100, choices=ESTADO_PEDIDO, default='pendiente')
    repartidor = models.ForeignKey(Repartidor, on_delete=models.SET_NULL, null=True, blank=True)

    def calcular_total(self):
        return sum(detalle.subtotal for detalle in self.detalles.all())

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.nombre}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE, related_name='detalles_pedido')
    cantidad = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    @property
    def subtotal(self):
        return self.plato.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.plato.nombre}"

class Menu(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='menus')
    fecha = models.DateField()
    platos = models.ManyToManyField(Plato)

    def __str__(self):
        return f"Menu {self.fecha} - {self.cliente.nombre}"
