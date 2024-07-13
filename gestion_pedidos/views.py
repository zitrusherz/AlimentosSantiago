from django.shortcuts import render, redirect

# Create your views here.
from .models import Pedido, Plato, DetallePedido
from .forms import PedidoForm, DetallePedidoForm
from .models import Menu
from .forms import MenuForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Cliente
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Sum
from django.db.models import Q


def buscar_pedidos(request):
    query = request.GET.get('q')
    if query:
        resultados = Pedido.objects.filter(
            Q(cliente__nombre__icontains=query) |
            Q(platos__nombre__icontains=query)
        ).distinct()
    else:
        resultados = Pedido.objects.none()

    return render(request, 'gestion_pedidos/buscar_pedidos.html', {
        'resultados': resultados,
        'query': query,
    })

def reportes(request):
    ventas_totales = Pedido.objects.aggregate(Sum('total'))
    pedidos_por_estado = Pedido.objects.values('estado').annotate(total=Sum('total'))
    return render(request, 'gestion_pedidos/reportes.html', {
        'ventas_totales': ventas_totales,
        'pedidos_por_estado': pedidos_por_estado,
    })
def crear_menu(request):
    if request.method == 'POST':
        menu_form = MenuForm(request.POST)
        if menu_form.is_valid():
            menu_form.save()
            return redirect('lista_menus')
    else:
        menu_form = MenuForm()
    return render(request, 'gestion_pedidos/crear_menu.html', {'menu_form': menu_form})

def lista_menus(request):
    menus = Menu.objects.all()
    return render(request, 'gestion_pedidos/lista_menus.html', {'menus': menus})
def catalogo(request):
    platos = Plato.objects.all()
    return render(request, 'gestion_pedidos/catalogo.html', {'platos': platos})

def crear_pedido(request):
    if request.method == 'POST':
        pedido_form = PedidoForm(request.POST)
        if pedido_form.is_valid():
            pedido = pedido_form.save()
            return redirect('detalle_pedido', pedido_id=pedido.id)
    else:
        pedido_form = PedidoForm()
    return render(request, 'gestion_pedidos/crear_pedido.html', {'pedido_form': pedido_form})

def detalle_pedido(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    if request.method == 'POST':
        detalle_form = DetallePedidoForm(request.POST)
        if detalle_form.is_valid():
            detalle_pedido = detalle_form.save(commit=False)
            detalle_pedido.pedido = pedido
            detalle_pedido.save()
            return redirect('detalle_pedido', pedido_id=pedido.id)
    else:
        detalle_form = DetallePedidoForm()
    detalles = DetallePedido.objects.filter(pedido=pedido)
    return render(request, 'gestion_pedidos/detalle_pedido.html', {
        'pedido': pedido,
        'detalle_form': detalle_form,
        'detalles': detalles,
    })
def lista_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'gestion_pedidos/lista_pedidos.html', {'pedidos': pedidos})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Cliente.objects.create(usuario=user, nombre=user.username, email=user.email)
            login(request, user)
            return redirect('catalogo')
    else:
        form = UserCreationForm()
    return render(request, 'gestion_pedidos/registration/register.html', {'form': form})

def enviar_notificacion_pedido(cliente_email, asunto, mensaje):
    send_mail(
        asunto,
        mensaje,
        settings.EMAIL_HOST_USER,
        [cliente_email],
        fail_silently=False,
    )