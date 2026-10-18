"""Conexión con las paqueterías para generar guías y consultar su estatus.

Las llamadas están simuladas: no salen a internet.
"""

import json
import random
from pathlib import Path

CREDENCIALES = Path(__file__).resolve().parent.parent / "config" / "credentials.json"


def _credenciales(paqueteria: str) -> dict:
    with open(CREDENCIALES, encoding="utf-8") as archivo:
        return json.load(archivo)["paqueterias"][paqueteria]


def generar_guia(paqueteria: str, codigo_postal: str, kilos: int) -> dict:
    """Solicita a la paquetería una guía de envío.

    Args:
        paqueteria: clave de la paquetería, "PRN" o "ECE".
        codigo_postal: código postal de destino.
        kilos: kilogramos cobrables del paquete.

    Returns:
        Diccionario con la paquetería y el número de guía.
    """
    _credenciales(paqueteria)
    return {"paqueteria": paqueteria, "guia": f"{paqueteria}{random.randint(10**9, 10**10 - 1)}"}


def consultar_estatus(paqueteria: str, guia: str) -> str:
    """Consulta el estatus de una guía tal como lo reporta la paquetería.

    Args:
        paqueteria: clave de la paquetería, "PRN" o "ECE".
        guia: número de guía.

    Returns:
        El código de estatus propio de la paquetería, sin normalizar.
    """
    _credenciales(paqueteria)
    codigos = {"PRN": ["RECOLECTADO", "EN_RUTA", "ENTREGADO", "DEVUELTO"], "ECE": ["01", "02", "03", "09"]}
    return random.choice(codigos[paqueteria])
