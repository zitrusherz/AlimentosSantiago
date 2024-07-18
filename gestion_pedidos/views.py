# gestion_pedidos/views.py

from django.utils import timezone
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from .forms import PedidoForm, DetallePedidoForm, MenuForm
from .models import Pedido, DetallePedido, Menu, Plato, CarroItem
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
    ventas_totales = Pedido.objects.aggregate(total=Sum('calcular_total'))['total']
    pedidos_por_estado = Pedido.objects.values('estado').annotate(total=Sum('calcular_total'))
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

# Vista del catálogo de platos
def catalogo(request):
    platos = Plato.objects.all()
    return render(request, 'gestion_pedidos/catalogo.html', {'platos': platos})

# Enviar notificaciones por correo
def enviar_notificacion_pedido(cliente_email, asunto, mensaje):
    send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, [cliente_email], fail_silently=False)

@login_required
def carro(request):
    # Asegurar que cada usuario tenga un pedido activo
    pedido, created = Pedido.objects.get_or_create(usuario=request.user, estado='pendiente')

    if request.method == 'POST':
        plato_id = request.POST.get('plato_id')
        cantidad = int(request.POST.get('cantidad', 1))
        plato = get_object_or_404(Plato, id=plato_id)
        carro_item, created = CarroItem.objects.get_or_create(usuario=request.user, plato=plato)
        carro_item.cantidad += cantidad
        carro_item.save()
        return redirect('carro')

    items = CarroItem.objects.filter(usuario=request.user)
    total = sum(item.subtotal for item in items)
    return render(request, 'gestion_pedidos/carro.html', {'items': items, 'total': total})

def agregar_al_carro(request, plato_id):
    carro = request.session.get('carro', {})
    cantidad = request.POST.get('cantidad', 1)

    if plato_id in carro:
        carro[plato_id] = carro.get(plato_id, 0) + int(cantidad)
    else:
        carro[plato_id] = int(cantidad)

    request.session['carro'] = carro
    return redirect('catalogo')

def ver_carro(request):
    carro = request.session.get('carro', {})
    platos = Plato.objects.filter(id__in=carro.keys())
    total = 0
    items = []

    for plato in platos:
        subtotal = plato.precio * carro[str(plato.id)]
        total += subtotal
        items.append({
            'plato': plato,
            'cantidad': carro[str(plato.id)],
            'subtotal': subtotal,
        })

    return render(request, 'gestion_pedidos/ver_carro.html', {'items': items, 'total': total})

@login_required
def checkout(request):
    carro = request.session.get('carro', {})
    if not carro:
        return redirect('carro')  # Redirigir al carro si está vacío

    try:
        with transaction.atomic():
            # Crear el pedido
            pedido = Pedido.objects.create(
                usuario=request.user,
                fecha_hora_entrega=timezone.now(),
                estado='pendiente'
            )

            # Crear los detalles del pedido
            for plato_id, cantidad in carro.items():
                plato = Plato.objects.get(id=plato_id)
                DetallePedido.objects.create(pedido=pedido, plato=plato, cantidad=cantidad)

            # Limpiar el carro de la sesión después de un checkout exitoso
            del request.session['carro']
            return redirect('orden_completada')

    except Exception as e:
        # Si ocurre un error, el pedido no se procesa y el carro de compras se mantiene igual
        return render(request, 'gestion_pedidos/checkout_error.html', {'error': str(e)})