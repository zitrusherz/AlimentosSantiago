from django import template

register = template.Library()

@register.filter
def es_usuario_empresa(user):
    return user.is_authenticated and user.email.endswith('@elcomilon.com')
