from django import template

register = template.Library()

@register.filter
def div(value, arg):
    """
    Divides the value by the arg.
    Usage: {{ value|div:arg }}
    Returns 0 if arg is 0 to prevent ZeroDivisionError.
    """
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0.0

@register.filter
def mul(value, arg):
    """
    Multiplies the value by the arg.
    Usage: {{ value|mul:arg }}
    """
    try:
        return float(value) * float(arg)
    except ValueError:
        return 0.0
