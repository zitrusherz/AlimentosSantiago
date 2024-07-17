from django import template

register = template.Library()

@register.filter
def to(value, arg):
    """Creates a range of numbers from value to arg (inclusive)."""
    return range(int(value), int(arg) + 1)
