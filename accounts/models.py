# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from gestion_pedidos.models import Cliente

class CustomUser(AbstractUser):
    @property
    def es_usuario_empresa(self):
        return self.email.endswith('@elcomilon.com')

    @property
    def cliente_profile(self):
        # Esto retorna el objeto Cliente asociado al usuario, si existe
        return Cliente.objects.filter(usuario=self).first()
