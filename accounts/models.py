from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    pass

    @property
    def es_usuario_empresa(self):
        return self.email.endswith('@elcomilon.com')
