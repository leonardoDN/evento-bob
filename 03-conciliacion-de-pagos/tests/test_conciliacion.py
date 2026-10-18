import os
import sys
import unittest
from collections import Counter
from decimal import Decimal
from pathlib import Path

# Las pruebas usan un banco que siempre responde y sin demora.
os.environ["BANCO_PROB_FALLA"] = "0"
os.environ["BANCO_DEMORA_MIN"] = "0"
os.environ["BANCO_DEMORA_MAX"] = "0"

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from conciliacion import cargar_cuentas_por_cobrar, cargar_pagos, conciliar_pago  # noqa: E402


class PruebasConciliacion(unittest.TestCase):
    def setUp(self):
        self.cuentas = cargar_cuentas_por_cobrar(RAIZ / "datos" / "cuentas_por_cobrar.csv")
        self.pagos = cargar_pagos(RAIZ / "datos" / "pagos_del_dia.csv")

    def resultado(self, referencia):
        pago = next(p for p in self.pagos if p["referencia"] == referencia)
        return conciliar_pago(pago, self.cuentas)

    def test_pago_exacto(self):
        self.assertEqual(self.resultado("A-1041")["resultado"], "conciliado")

    def test_diferencia_dentro_de_tolerancia(self):
        self.assertEqual(self.resultado("A-1046")["resultado"], "conciliado")

    def test_pago_parcial(self):
        r = self.resultado("A-1044")
        self.assertEqual(r["resultado"], "pago_parcial")
        self.assertIn("1,480.00", r["detalle"])

    def test_pago_en_exceso(self):
        self.assertEqual(self.resultado("A-1051")["resultado"], "pago_en_exceso")

    def test_transferencia_devuelta(self):
        self.assertEqual(self.resultado("A-1047")["resultado"], "no_liquidada")

    def test_referencia_mal_escrita(self):
        self.assertEqual(self.resultado("A1050")["resultado"], "sin_factura")

    def test_referencia_en_minusculas(self):
        self.assertEqual(self.resultado("a-1056")["resultado"], "conciliado")

    def test_resumen_del_dia(self):
        resumen = Counter(conciliar_pago(p, self.cuentas)["resultado"] for p in self.pagos)
        self.assertEqual(resumen, {"conciliado": 8, "pago_parcial": 1, "pago_en_exceso": 1, "no_liquidada": 1, "sin_factura": 1})
        self.assertEqual(sum(p["importe"] for p in self.pagos), Decimal("268232.20"))


if __name__ == "__main__":
    unittest.main()
