from decimal import Decimal

from app.costos import costo_orden, importe_refaccion


def test_importe_refaccion_con_precio_flotante():
    assert importe_refaccion(1240.0, 3) == Decimal("3720.00")


def test_costo_solo_mano_de_obra():
    c = costo_orden(2, [])
    assert c["subtotal"] == Decimal("1700.00")
    assert c["iva"] == Decimal("272.00")
    assert c["total"] == Decimal("1972.00")


def test_costo_con_refacciones():
    c = costo_orden(0.5, [Decimal("3850.00"), Decimal("450.00")])
    assert c["costo_mano_obra"] == Decimal("425.00")
    assert c["costo_refacciones"] == Decimal("4300.00")
    assert c["total"] == Decimal("5481.00")
