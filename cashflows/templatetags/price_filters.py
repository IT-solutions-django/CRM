from django import template
from decimal import Decimal, ROUND_HALF_UP

register = template.Library()


@register.filter(name='price_format')
def price_format(value: Decimal) -> Decimal:
    try:
        value = Decimal(value).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return f"{value:,}".replace(',', ' ').replace('.', ',')
    except (ValueError, TypeError):
        return value

@register.filter(name='price_int_format')
def price_format(value: Decimal) -> int:
    try:
        value = Decimal(value).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        value = int(value)
        return f"{value:,}".replace(',', ' ').replace('.', ',')
    except (ValueError, TypeError):
        return value