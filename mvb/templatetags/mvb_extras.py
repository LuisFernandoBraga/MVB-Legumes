from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Permite acessar itens de um dicionário por chave."""
    if not dictionary:
        return None
    return dictionary.get(str(key)) or dictionary.get(key)

@register.filter
def mul(a, b):
    """Multiplicação segura para template."""
    try:
        return float(a) * float(b)
    except:
        return 0

@register.filter
def first_existing(obj, attrs):
    """
    Retorna o primeiro atributo existente e não nulo
    Exemplo: {{ objeto|first_existing:"valor_por_caixa,valor_rendido" }}
    """
    for attr in attrs.split(","):
        attr = attr.strip()
        if hasattr(obj, attr):
            val = getattr(obj, attr)
            if val not in (None, "", 0):
                return val
    return 0