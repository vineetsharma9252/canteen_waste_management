from django import template #type:ignore

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


@register.filter
def unique(lst, key):
    """
    Returns a list of unique items from the given list based on the specified key.
    """
    seen = set()
    unique_list = []
    for item in lst:
        item_key = item.get(key)
        if item_key not in seen:
            seen.add(item_key)
            unique_list.append(item)
    return unique_list