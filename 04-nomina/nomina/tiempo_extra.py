"""Pago de horas extra de la semana."""

from decimal import Decimal

from nomina.prestaciones import redondear

HORAS_DOBLES_POR_SEMANA = 9


def pago_tiempo_extra(salario_por_hora: Decimal, horas_extra: Decimal) -> Decimal:
    """Calcula el pago de las horas extra de una semana.

    Las primeras nueve horas extra de la semana se pagan al doble y las que
    pasen de nueve, al triple.

    Args:
        salario_por_hora: salario ordinario por hora.
        horas_extra: horas extra trabajadas en la semana.

    Returns:
        Importe a pagar, redondeado a centavos.
    """
    dobles = min(horas_extra, HORAS_DOBLES_POR_SEMANA)
    triples = max(horas_extra - HORAS_DOBLES_POR_SEMANA, 0)
    return redondear(salario_por_hora * (2 * dobles + 3 * triples))
