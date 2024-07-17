from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum, Q
from .forms import PedidoForm, DetallePedidoForm, MenuForm, CustomUserCreationForm
from .models import Pedido, DetallePedido, Menu, Cliente, Plato
from django.core.mail import send_mail
from django.conf import settings

# Busca pedidos basados en una consulta del usuario
def buscar_pedidos(request):
    query = request.GET.get('q', '')
    resultados = Pedido.objects.filter(
        Q(cliente__nombre__icontains=query) |
        Q(platos__nombre__icontains=query)
    ).distinct() if query else Pedido.objects.none()
    return render(request, 'gestion_pedidos/buscar_pedidos.html', {'resultados': resultados, 'query': query})

# Muestra reportes de ventas y pedidos
def reportes(request):
    ventas_totales = Pedido.objects.aggregate(total=Sum('total'))['total']
    pedidos_por_estado = Pedido.objects.values('estado').annotate(total=Sum('total'))
    return render(request, 'gestion_pedidos/reportes.html', {
        'ventas_totales': ventas_totales,
        'pedidos_por_estado': pedidos_por_estado,
    })

# Crea un nuevo menú
@login_required
def crear_menu(request):
    menu_form = MenuForm(request.POST or None)
    if request.method == 'POST' and menu_form.is_valid():
        menu_form.save()
        return redirect('lista_menus')
    return render(request, 'gestion_pedidos/crear_menu.html', {'menu_form': menu_form})

# Lista todos los menús disponibles
@login_required
def lista_menus(request):
    menus = Menu.objects.all()
    return render(request, 'gestion_pedidos/lista_menus.html', {'menus': menus})

# Vista principal del sitio
def index(request):
    platos = Plato.objects.all()[:6]  # Mostrar solo los primeros 6 platos
    featured_platos = Plato.objects.filter(featured=True)
    numbers = list(range(1, 13))  # Crear la lista de números del 1 al 12
    return render(request, 'gestion_pedidos/index.html', {
        'platos': platos,
        'featured_platos': featured_platos,
        'numbers': numbers
    })

# Crea un nuevo pedido
@login_required
def crear_pedido(request):
    pedido_form = PedidoForm(request.POST or None)
    if pedido_form.is_valid():
        pedido = pedido_form.save()
        return redirect('detalle_pedido', pedido_id=pedido.id)
    return render(request, 'gestion_pedidos/crear_pedido.html', {'pedido_form': pedido_form})

# Detalle de pedido específico
@login_required
def detalle_pedido(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    detalle_form = DetallePedidoForm(request.POST or None)
    if request.method == 'POST' and detalle_form.is_valid():
        detalle_pedido = detalle_form.save(commit=False)
        detalle_pedido.pedido = pedido
        detalle_pedido.save()
        return redirect('detalle_pedido', pedido_id=pedido.id)
    detalles = DetallePedido.objects.filter(pedido=pedido)
    return render(request, 'gestion_pedidos/detalle_pedido.html', {
        'pedido': pedido,
        'detalle_form': detalle_form,
        'detalles': detalles,
    })

# Lista todos los pedidos
@login_required
def lista_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'gestion_pedidos/lista_pedidos.html', {'pedidos': pedidos})

# Registro de usuarios
def register(request):
    form = CustomUserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        Cliente.objects.create(usuario=user, nombre=user.username, email=user.email)
        login(request, user)
        return redirect('index')
    return render(request, 'gestion_pedidos/registration/register.html', {'form': form})

# Autenticación de usuario
def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
    return render(request, 'gestion_pedidos/registration/login.html', {'form': form})

# Cierre de sesión
def logout_view(request):
    logout(request)
    return redirect('index')

# Vista del catálogo de platos
def catalogo(request):
    platos = Plato.objects.all()
    return render(request, 'gestion_pedidos/catalogo.html', {'platos': platos})

# Enviar notificaciones por correo
def enviar_notificacion_pedido(cliente_email, asunto, mensaje):
    send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, [cliente_email], fail_silently=False)
