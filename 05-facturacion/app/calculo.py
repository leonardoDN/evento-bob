"""Cálculo de importes de pedidos."""

from decimal import ROUND_HALF_UP, Decimal

TASA_IVA = Decimal("0.16")
CENTAVO = Decimal("0.01")


def redondear(valor: Decimal) -> Decimal:
    """Redondea a centavos con el criterio del SAT (mitad hacia arriba)."""
    return valor.quantize(CENTAVO, rounding=ROUND_HALF_UP)


def importe_renglon(precio: Decimal, cantidad: int) -> Decimal:
    return redondear(Decimal(str(precio)) * cantidad)


def totales(importes: list[Decimal]) -> dict:
    """Calcula subtotal, IVA y total a partir de los importes de cada renglón."""
    subtotal = redondear(sum(importes, Decimal("0")))
    iva = redondear(subtotal * TASA_IVA)
    return {"subtotal": subtotal, "iva": iva, "total": subtotal + iva}
