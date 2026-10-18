"""Ronda 3: importes de los conceptos y totales del CFDI."""


def calcular_conceptos(renglones):
    """Calcula importe e IVA por concepto y los totales del comprobante.

    Args:
        renglones: lista de diccionarios con "precio" y "cantidad".
    """
    conceptos = []
    for r in renglones:
        importe = round(r["precio"] * r["cantidad"], 2)
        iva = round(importe * 0.16, 2)
        conceptos.append({"importe": importe, "iva": iva})

    subtotal = round(sum(r["precio"] * r["cantidad"] for r in renglones), 2)
    iva_total = round(subtotal * 0.16, 2)
    precio_promedio = subtotal / sum(r["cantidad"] for r in renglones)
    return {
        "conceptos": conceptos,
        "subtotal": subtotal,
        "iva": iva_total,
        "total": subtotal + iva_total,
        "precio_promedio": precio_promedio,
    }
