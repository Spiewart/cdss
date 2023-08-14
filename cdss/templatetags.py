from django.template.defaulttags import register  # type: ignore

...


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_item_less_3000(dictionary, key):
    return dictionary.get(key - 3000)
