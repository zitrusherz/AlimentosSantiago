from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    @property
    def es_usuario_empresa(self):
        return self.email.endswith('@elcomilon.com')

    @property
    def cliente_profile(self):
        return self.cliente if hasattr(self, 'cliente') else None