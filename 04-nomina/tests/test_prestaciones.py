import unittest
from datetime import date
from decimal import Decimal

from nomina.prestaciones import aguinaldo, antiguedad, dias_de_vacaciones, prima_vacacional
from nomina.tiempo_extra import pago_tiempo_extra


class PruebasPrestaciones(unittest.TestCase):
    def test_antiguedad(self):
        self.assertEqual(antiguedad(date(2020, 10, 20), date(2026, 10, 19)), 5)
        self.assertEqual(antiguedad(date(2020, 10, 20), date(2026, 10, 20)), 6)
        self.assertEqual(antiguedad(date(2026, 3, 1), date(2026, 10, 20)), 0)

    def test_dias_de_vacaciones(self):
        self.assertEqual(dias_de_vacaciones(0), 0)
        self.assertEqual(dias_de_vacaciones(1), 6)
        self.assertEqual(dias_de_vacaciones(4), 12)
        self.assertEqual(dias_de_vacaciones(5), 14)
        self.assertEqual(dias_de_vacaciones(10), 16)

    def test_prima_vacacional(self):
        self.assertEqual(prima_vacacional(Decimal("410.00"), 8), Decimal("820.00"))

    def test_aguinaldo_completo_y_proporcional(self):
        self.assertEqual(aguinaldo(Decimal("540.00"), 365), Decimal("8100.00"))
        self.assertEqual(aguinaldo(Decimal("620.00"), 304), Decimal("7745.75"))

    def test_tiempo_extra(self):
        self.assertEqual(pago_tiempo_extra(Decimal("60.00"), Decimal("6")), Decimal("720.00"))
        self.assertEqual(pago_tiempo_extra(Decimal("60.00"), Decimal("12")), Decimal("1620.00"))


if __name__ == "__main__":
    unittest.main()
