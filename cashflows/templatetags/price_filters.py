from django import template


register = template.Library()


@register.filter(name='price_format')
def price_format(value: str):
    try:
        value = value
        return f"{value:,}".replace(',', ' ').replace('.', ',')
    except (ValueError, TypeError):
        return value
