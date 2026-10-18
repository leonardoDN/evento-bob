"""Muestra las prestaciones de la plantilla a una fecha de corte.

Uso: python calcular_prestaciones.py [AAAA-MM-DD]
"""

import csv
import sys
from datetime import date
from decimal import Decimal
from pathlib import Path

from nomina.prestaciones import aguinaldo, antiguedad, dias_de_vacaciones, prima_vacacional

PLANTILLA = Path(__file__).resolve().parent / "datos" / "plantilla.csv"


def main() -> int:
    corte = date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else date.today()
    inicio_del_anio = date(corte.year, 1, 1)
    dias_del_anio = (date(corte.year + 1, 1, 1) - inicio_del_anio).days
    print(f"Prestaciones al {corte:%d/%m/%Y}\n")
    print(f"{'Nombre':<20} {'Años':>4} {'Vacaciones':>10} {'Prima vac.':>12} {'Aguinaldo':>12}")

    with open(PLANTILLA, encoding="utf-8", newline="") as archivo:
        for t in csv.DictReader(archivo):
            ingreso = date.fromisoformat(t["fecha_ingreso"])
            salario = Decimal(t["salario_diario"])
            anios = antiguedad(ingreso, corte)
            dias = dias_de_vacaciones(anios)
            trabajados = (date(corte.year, 12, 31) - max(ingreso, inicio_del_anio)).days + 1
            print(
                f"{t['nombre']:<20} {anios:>4} {dias:>10} {prima_vacacional(salario, dias):>12,.2f} "
                f"{aguinaldo(salario, trabajados, dias_del_anio):>12,.2f}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
