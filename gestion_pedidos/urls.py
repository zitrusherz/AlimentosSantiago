from django.urls import path
from .views import (
    index, buscar_pedidos, reportes, crear_menu, lista_menus,
    crear_pedido, detalle_pedido, lista_pedidos, catalogo
)
from accounts.views import register, login_view, logout_view

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
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
