from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('buscar/', views.buscar_pedidos, name='buscar_pedidos'),
    path('reportes/', views.reportes, name='reportes'),
    path('menu/nuevo/', views.crear_menu, name='crear_menu'),
    path('menus/', views.lista_menus, name='lista_menus'),
    path('pedido/nuevo/', views.crear_pedido, name='crear_pedido'),
    path('pedido/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('carro/', views.ver_carro, name='ver_carro'),
    path('carro/agregar/<int:plato_id>/', views.agregar_al_carro, name='agregar_al_carro'),
    path('carro/eliminar_unidad/<int:plato_id>/', views.eliminar_unidad_del_carro, name='eliminar_unidad_del_carro'),
    path('carro/eliminar/<int:plato_id>/', views.eliminar_del_carro, name='eliminar_del_carro'),
    path('checkout/', views.checkout, name='checkout'),
]
