import re
from django.core.exceptions import ValidationError

def validate_cpf(value):
    """
    Valida CPF (somente dígitos). Aceita com ou sem pontuação.
    Implementa cálculo dos dois dígitos verificadores.
    """
    if not value:
        raise ValidationError("CPF inválido.")
    # remover não dígitos
    cpf = re.sub(r'[^0-9]', '', value)
    if len(cpf) != 11:
        raise ValidationError("CPF deve ter 11 dígitos.")

    # CPFs com todos dígitos iguais são inválidos (ex: 11111111111)
    if cpf == cpf[0] * 11:
        raise ValidationError("CPF inválido.")

    def calc_dv(digs):
        s = sum(int(d) * w for d, w in zip(digs, range(len(digs)+1, 1, -1)))
        r = 11 - (s % 11)
        return '0' if r >= 10 else str(r)

    dv1 = calc_dv(cpf[:9])
    dv2 = calc_dv(cpf[:9] + dv1)
    if cpf[-2:] != dv1 + dv2:
        raise ValidationError("CPF inválido.")