"""Ronda 1: ¿cuántas piezas faltan para surtir un pedido?"""


def piezas_faltantes(renglones, existencias):
    """Devuelve las piezas que faltan, por SKU, para surtir completo el pedido.

    Args:
        renglones: lista de diccionarios con "sku" y "cantidad".
        existencias: diccionario {sku: piezas en almacén}.
    """
    faltantes = {}
    total_piezas = 0
    for i in range(1, len(renglones)):
        sku = renglones[i]["sku"]
        pedido = renglones[i]["cantidad"]
        disponible = existencias.get(sku, 0)
        if pedido > disponible:
            faltantes[sku] = pedido - disponible
    return faltantes
