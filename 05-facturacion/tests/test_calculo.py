from decimal import Decimal

from app.calculo import importe_renglon, redondear, totales


def test_redondeo_mitad_hacia_arriba():
    assert redondear(Decimal("2.675")) == Decimal("2.68")
    assert redondear(Decimal("2.665")) == Decimal("2.67")


def test_importe_renglon_con_precio_flotante():
    assert importe_renglon(162.9, 3) == Decimal("488.70")


def test_totales():
    t = totales([Decimal("389.00"), Decimal("245.50")])
    assert t["subtotal"] == Decimal("634.50")
    assert t["iva"] == Decimal("101.52")
    assert t["total"] == Decimal("736.02")
