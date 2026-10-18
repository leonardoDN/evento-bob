"""Prestaciones de ley: vacaciones, prima vacacional y aguinaldo."""

from datetime import date
from decimal import ROUND_HALF_UP, Decimal

CENTAVO = Decimal("0.01")
PORCENTAJE_PRIMA_VACACIONAL = Decimal("0.25")
DIAS_AGUINALDO = 15


def redondear(valor: Decimal) -> Decimal:
    """Redondea a centavos, mitad hacia arriba.

    Args:
        valor: importe a redondear.

    Returns:
        El importe con dos decimales.
    """
    return valor.quantize(CENTAVO, rounding=ROUND_HALF_UP)


def antiguedad(fecha_ingreso: date, fecha_corte: date) -> int:
    """Calcula los años cumplidos de servicio a una fecha de corte.

    Args:
        fecha_ingreso: fecha en que el trabajador entró a la empresa.
        fecha_corte: fecha a la que se mide la antigüedad.

    Returns:
        Años completos de servicio; cero si aún no cumple el primero.
    """
    anios = fecha_corte.year - fecha_ingreso.year
    if (fecha_corte.month, fecha_corte.day) < (fecha_ingreso.month, fecha_ingreso.day):
        anios -= 1
    return max(anios, 0)


# Artículo 76 de la Ley Federal del Trabajo.
def dias_de_vacaciones(anios_cumplidos: int) -> int:
    if anios_cumplidos < 1:
        return 0
    if anios_cumplidos <= 4:
        return 6 + 2 * (anios_cumplidos - 1)
    return 12 + 2 * ((anios_cumplidos - 5) // 5 + 1)


def prima_vacacional(salario_diario: Decimal, dias_vacaciones: int) -> Decimal:
    """Calcula la prima vacacional, 25 % del salario de los días de vacaciones.

    Args:
        salario_diario: salario diario del trabajador.
        dias_vacaciones: días de vacaciones que le corresponden.

    Returns:
        Importe de la prima, redondeado a centavos.
    """
    return redondear(salario_diario * dias_vacaciones * PORCENTAJE_PRIMA_VACACIONAL)


def aguinaldo(salario_diario: Decimal, dias_trabajados: int, dias_del_anio: int = 365) -> Decimal:
    """Calcula el aguinaldo de 15 días, proporcional a lo trabajado en el año.

    Args:
        salario_diario: salario diario del trabajador.
        dias_trabajados: días trabajados en el año calendario.
        dias_del_anio: días del año calendario, 365 o 366.

    Returns:
        Importe del aguinaldo, redondeado a centavos.
    """
    proporcion = Decimal(min(dias_trabajados, dias_del_anio)) / Decimal(dias_del_anio)
    return redondear(salario_diario * DIAS_AGUINALDO * proporcion)
