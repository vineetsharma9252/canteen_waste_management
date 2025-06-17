from django import template

register = template.Library()

@register.filter
def split(value, delimiter=','):
    return value.split(delimiter)

@register.filter
def strip(value):
    return value.strip()

@register.filter
def default_if_none(value, default):
    return value if value is not None else default

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)