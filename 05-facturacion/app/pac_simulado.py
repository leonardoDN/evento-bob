"""Simulador del proveedor de certificación (PAC).

Imita al servicio real de timbrado: casi siempre responde, a veces tarda varios
segundos y de vez en cuando no contesta. No sale a internet.
"""

import os
import random
import time
import uuid


class PacNoDisponible(Exception):
    """El PAC no respondió a tiempo."""


# Probabilidad de que una llamada falle y rango de demora en segundos.
PROB_FALLA = float(os.environ.get("PAC_PROB_FALLA", "0.35"))
DEMORA_MIN = float(os.environ.get("PAC_DEMORA_MIN", "0.3"))
DEMORA_MAX = float(os.environ.get("PAC_DEMORA_MAX", "2.5"))


def solicitar_timbre(xml: str) -> dict:
    time.sleep(random.uniform(DEMORA_MIN, DEMORA_MAX))
    if random.random() < PROB_FALLA:
        raise PacNoDisponible("El PAC no respondió (tiempo de espera agotado)")
    return {
        "uuid": str(uuid.uuid4()).upper(),
        "fecha_timbrado": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "sello_sat": "SIMULADO",
    }


def solicitar_cancelacion(uuid_cfdi: str, motivo: str) -> dict:
    time.sleep(random.uniform(DEMORA_MIN, DEMORA_MAX))
    if random.random() < PROB_FALLA:
        raise PacNoDisponible("El PAC no respondió (tiempo de espera agotado)")
    return {"uuid": uuid_cfdi, "estatus": "Cancelado", "fecha": time.strftime("%Y-%m-%dT%H:%M:%S")}
