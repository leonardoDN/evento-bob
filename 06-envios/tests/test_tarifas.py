import unittest
from decimal import Decimal

from envios.rastreo import normalizar_estatus
from envios.tarifas import EnvioInvalido, cotizar, peso_cobrable, zona_destino


class PruebasTarifas(unittest.TestCase):
    def test_peso_cobrable_usa_el_mayor(self):
        self.assertEqual(peso_cobrable(2.0, 40, 30, 30), 8)
        self.assertEqual(peso_cobrable(12.3, 20, 20, 20), 13)

    def test_zonas(self):
        self.assertEqual(zona_destino("06600"), 1)
        self.assertEqual(zona_destino("64000"), 3)
        self.assertEqual(zona_destino("22000"), 5)
        self.assertEqual(zona_destino("44100"), 6)

    def test_cotizar(self):
        c = cotizar("97000", 2.0, 40, 30, 30)
        self.assertEqual(c, {"zona": 4, "kilos_cobrables": 8, "precio": Decimal("259.50")})

    def test_codigo_postal_invalido(self):
        with self.assertRaises(EnvioInvalido):
            zona_destino("6400")

    def test_peso_maximo(self):
        with self.assertRaises(EnvioInvalido):
            cotizar("64000", 80, 10, 10, 10)

    def test_estatus_desconocido(self):
        self.assertEqual(normalizar_estatus("ECE", "77"), "incidencia")


if __name__ == "__main__":
    unittest.main()
