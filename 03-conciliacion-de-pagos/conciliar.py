"""Corre la conciliación del día y muestra el resultado de cada pago.

Uso: python conciliar.py
"""

from collections import Counter
from pathlib import Path

from banco_simulado import BancoNoDisponible
from conciliacion import cargar_cuentas_por_cobrar, cargar_pagos, conciliar_pago

DATOS = Path(__file__).resolve().parent / "datos"


def main() -> int:
    cuentas = cargar_cuentas_por_cobrar(DATOS / "cuentas_por_cobrar.csv")
    pagos = cargar_pagos(DATOS / "pagos_del_dia.csv")
    print(f"Conciliación de {len(pagos)} pagos recibidos por SPEI\n")

    resultados = []
    for numero, pago in enumerate(pagos, start=1):
        try:
            r = conciliar_pago(pago, cuentas)
        except BancoNoDisponible as e:
            print(f"\nSe interrumpió en el pago {numero} de {len(pagos)}: {e}.")
            print("La conciliación quedó a medias y hay que volver a correrla completa.")
            return 1
        resultados.append(r)
        print(f"{numero:>3}  {r['ordenante'][:34]:<34} {r['importe']:>12,.2f}  {r['resultado']:<15} {r['detalle']}")

    resumen = Counter(r["resultado"] for r in resultados)
    print("\nResumen: " + ", ".join(f"{cantidad} {resultado}" for resultado, cantidad in resumen.most_common()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
