from django.apps import AppConfig



class GestionPedidosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestion_pedidos'

    def ready(self):
        import gestion_pedidos.signals