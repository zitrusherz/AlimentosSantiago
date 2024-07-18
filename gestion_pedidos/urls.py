# gestion_pedidos/urls.py

from django.urls import path
from .views import (
    index, buscar_pedidos, reportes, crear_menu, lista_menus,
    crear_pedido, detalle_pedido, lista_pedidos, catalogo,
    carro, agregar_al_carro, ver_carro, checkout
)

urlpatterns = [
    path('', index, name='index'),
    path('buscar/', buscar_pedidos, name='buscar_pedidos'),
    path('reportes/', reportes, name='reportes'),
    path('menu/nuevo/', crear_menu, name='crear_menu'),
    path('menus/', lista_menus, name='lista_menus'),
    path('pedido/nuevo/', crear_pedido, name='crear_pedido'),
    path('pedido/<int:pedido_id>/', detalle_pedido, name='detalle_pedido'),
    path('pedidos/', lista_pedidos, name='lista_pedidos'),
    path('catalogo/', catalogo, name='catalogo'),
    path('carro/', carro, name='carro'),
    path('agregar_al_carro/<int:plato_id>/', agregar_al_carro, name='agregar_al_carro'),
    path('ver_carro/', ver_carro, name='ver_carro'),
    path('checkout/', checkout, name='checkout'),
]
