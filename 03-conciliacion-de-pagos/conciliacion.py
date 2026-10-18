"""Conciliación de los pagos recibidos por SPEI contra las facturas por cobrar."""

import csv
from decimal import Decimal
from pathlib import Path

import banco_simulado

# Diferencias de hasta un peso se dan por buenas (comisiones y redondeos del cliente).
TOLERANCIA = Decimal("1.00")


def cargar_cuentas_por_cobrar(ruta: Path) -> dict[str, dict]:
    """Lee las facturas pendientes de cobro, indexadas por folio."""
    with open(ruta, encoding="utf-8", newline="") as archivo:
        return {
            fila["folio"]: {**fila, "saldo": Decimal(fila["saldo"])}
            for fila in csv.DictReader(archivo)
        }


def cargar_pagos(ruta: Path) -> list[dict]:
    """Lee los pagos que llegaron en el estado de cuenta del día."""
    with open(ruta, encoding="utf-8", newline="") as archivo:
        return [{**fila, "importe": Decimal(fila["importe"])} for fila in csv.DictReader(archivo)]


def conciliar_pago(pago: dict, cuentas: dict[str, dict]) -> dict:
    estado = banco_simulado.consultar_transferencia(pago["clave_rastreo"])

    if estado["estatus"] != "LIQUIDADA":
        return {**pago, "resultado": "no_liquidada", "detalle": f"El banco la reporta {estado['estatus'].lower()}"}

    cuenta = cuentas.get(pago["referencia"].strip().upper())
    if cuenta is None:
        return {**pago, "resultado": "sin_factura", "detalle": "La referencia no corresponde a ninguna factura pendiente"}

    diferencia = pago["importe"] - cuenta["saldo"]
    if abs(diferencia) <= TOLERANCIA:
        return {**pago, "resultado": "conciliado", "detalle": f"Factura {cuenta['folio']}"}
    if diferencia < 0:
        return {**pago, "resultado": "pago_parcial", "detalle": f"Faltan {-diferencia:,.2f} de la factura {cuenta['folio']}"}
    return {**pago, "resultado": "pago_en_exceso", "detalle": f"Sobran {diferencia:,.2f} sobre la factura {cuenta['folio']}"}
