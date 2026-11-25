from django import template

from accesos.permisos import puede_modificar as _puede_modificar

register = template.Library()


@register.filter
def puede_modificar(objeto, usuario):
    """Se usa en plantillas así: {% if registro|puede_modificar:user %}"""
    return _puede_modificar(usuario, objeto)