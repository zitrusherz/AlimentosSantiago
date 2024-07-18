from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Proveedor(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    contacto = models.CharField(max_length=200)
    telefono = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cliente_profile')
    nombre = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, validators=[MinValueValidator(0)])

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

class Descuento(models.Model):
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE, related_name='descuentos')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='descuentos')
    porcentaje_descuento = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return f"{self.porcentaje_descuento}% off {self.plato.nombre} for {self.cliente.nombre}"

class Repartidor(models.Model):
    nombre = models.CharField(max_length=200)
    telefono = models.CharField(max_length=50)
    rutas = models.TextField()

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pedidos')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos')  # Agregar campo cliente
    ESTADO_PEDIDO = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('en_camino', 'En Camino'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]

    platos = models.ManyToManyField(Plato, through='DetallePedido')
    fecha_hora_pedido = models.DateTimeField(default=timezone.now)
    fecha_hora_entrega = models.DateTimeField()
    estado = models.CharField(max_length=100, choices=ESTADO_PEDIDO, default='pendiente')
    repartidor = models.ForeignKey(Repartidor, on_delete=models.SET_NULL, null=True, blank=True)

    def calcular_total(self):
        total = 0
        for detalle in self.detalles.all():
            descuento = detalle.plato.descuentos.filter(cliente=self.usuario.cliente_profile, fecha_inicio__lte=timezone.now(), fecha_fin__gte=timezone.now()).first()
            if descuento:
                total += detalle.subtotal * (1 - (descuento.porcentaje_descuento / 100))
            else:
                total += detalle.subtotal
        return total

    def __str__(self):
        return f"Pedido {self.id} - {self.usuario}"

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

class CarroItem(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carro_items')
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.plato.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad} de {self.plato.nombre}"
