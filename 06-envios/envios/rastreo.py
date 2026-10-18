"""Traduce los estatus de cada paquetería a un estatus único del sistema."""

ESTATUS = {
    "PRN": {"RECOLECTADO": "en_transito", "EN_RUTA": "en_transito", "ENTREGADO": "entregado", "DEVUELTO": "devuelto"},
    "ECE": {"01": "en_transito", "02": "en_transito", "03": "entregado", "09": "devuelto"},
}


def normalizar_estatus(paqueteria: str, estatus: str) -> str:
    """Convierte el estatus de una paquetería al estatus del sistema.

    Args:
        paqueteria: clave de la paquetería, "PRN" o "ECE".
        estatus: código de estatus tal como lo reporta la paquetería.

    Returns:
        "en_transito", "entregado", "devuelto", o "incidencia" si el código no se conoce.
    """
    return ESTATUS.get(paqueteria, {}).get(estatus, "incidencia")
