from django import template

register = template.Library()

@register.filter
def get_attr(obj, get_attr):
    return getattr(obj, get_attr, None)

