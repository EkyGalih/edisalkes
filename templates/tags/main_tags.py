from django import template
register = template.Library()

@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def pengurangan(value,arg):
    return value - arg

@register.filter
def format_rupiah(q):
    try:
        if isinstance(q, str):
            q = int(q)
        
        currency = "Rp. {:,}".format(q)
        currency = currency.replace(",", ".")
        
        return currency
    except:
        return None