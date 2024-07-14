from django import template

register = template.Library()

@register.filter
def concat(val1, val2):
    return f"{val1}{val2}"
