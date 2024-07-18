from datetime import timedelta
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

# Agregar un plato al carrito
@login_required
def agregar_al_carro(request, plato_id):
    carro = request.session.get('carro', {})
    cantidad = request.POST.get('cantidad', 1)
    plato_id = str(plato_id)

    if plato_id in carro:
        carro[plato_id] = carro.get(plato_id, 0) + int(cantidad)
    else:
        carro[plato_id] = int(cantidad)

    request.session['carro'] = carro
    return redirect('catalogo')

# Ver el carrito
@login_required
def ver_carro(request):
    carro = request.session.get('carro', {})
    platos = Plato.objects.filter(id__in=carro.keys())
    total = 0
    items = []

    for plato in platos:
        item_id = plato.id
        cantidad = carro[str(item_id)]
        subtotal = plato.precio * cantidad
        total += subtotal
        items.append({
            'id': item_id,
            'plato': plato,
            'cantidad': cantidad,
            'subtotal': subtotal,
        })

    return render(request, 'gestion_pedidos/ver_carro.html', {'items': items, 'total': total})

# Eliminar un plato del carrito
@login_required
def eliminar_del_carro(request, plato_id):
    carro = request.session.get('carro', {})
    plato_id = str(plato_id)
    if plato_id in carro:
        del carro[plato_id]
    request.session['carro'] = carro
    return redirect('ver_carro')

# Eliminar una unidad de un plato del carrito
@login_required
def eliminar_unidad_del_carro(request, plato_id):
    carro = request.session.get('carro', {})
    plato_id = str(plato_id)
    if plato_id in carro:
        if carro[plato_id] > 1:
            carro[plato_id] -= 1
        else:
            del carro[plato_id]
    request.session['carro'] = carro
    return redirect('ver_carro')

# Realizar el checkout
@login_required
def checkout(request):
    try:
        carro = request.session.get('carro', {})
        if not carro:
            return redirect('ver_carro')  # Redirige al carro si está vacío

        fecha_hora_entrega = timezone.now() + timedelta(minutes=30)
        with transaction.atomic():
            pedido = Pedido.objects.create(
                usuario=request.user,
                cliente=request.user.cliente_profile,
                fecha_hora_entrega=fecha_hora_entrega,
                estado='pendiente'
            )
            for plato_id, cantidad in carro.items():
                plato = get_object_or_404(Plato, id=plato_id)
                DetallePedido.objects.create(pedido=pedido, plato=plato, cantidad=cantidad)

        request.session['carro'] = {}  # Limpiar el carro de la sesión
        return redirect('orden_completada')
    except Exception as e:
        # En caso de cualquier error, redirige a la página de error
        return render(request, 'gestion_pedidos/checkout_error.html', {'error': str(e)})
