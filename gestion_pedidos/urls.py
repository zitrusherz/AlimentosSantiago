from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.catalogo, name='catalogo'),
    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('crear_pedido/', views.crear_pedido, name='crear_pedido'),
    path('detalle_pedido/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
    path('menus/', views.lista_menus, name='lista_menus'),
    path('crear_menu/', views.crear_menu, name='crear_menu'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('buscar_pedidos/', views.buscar_pedidos, name='buscar_pedidos'),
]
