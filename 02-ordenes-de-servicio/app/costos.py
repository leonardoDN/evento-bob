"""Cálculo del costo de una orden de servicio."""

from decimal import ROUND_HALF_UP, Decimal

TARIFA_HORA = Decimal("850.00")
TASA_IVA = Decimal("0.16")
CENTAVO = Decimal("0.01")


def redondear(valor: Decimal) -> Decimal:
    """Redondea a centavos, mitad hacia arriba."""
    return valor.quantize(CENTAVO, rounding=ROUND_HALF_UP)


def importe_refaccion(precio, cantidad: int) -> Decimal:
    return redondear(Decimal(str(precio)) * cantidad)


def costo_orden(horas, importes_refacciones: list[Decimal]) -> dict:
    """Mano de obra a tarifa fija más refacciones, con IVA."""
    mano_obra = redondear(Decimal(str(horas)) * TARIFA_HORA)
    refacciones = redondear(sum(importes_refacciones, Decimal("0")))
    subtotal = mano_obra + refacciones
    iva = redondear(subtotal * TASA_IVA)
    return {
        "costo_mano_obra": mano_obra,
        "costo_refacciones": refacciones,
        "subtotal": subtotal,
        "iva": iva,
        "total": subtotal + iva,
    }
