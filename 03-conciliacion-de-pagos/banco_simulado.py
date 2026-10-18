"""Simulador del servicio del banco para consultar transferencias SPEI.

Imita al servicio real: casi siempre responde, a veces tarda y de vez en cuando
no contesta. No sale a internet.
"""

import os
import random
import time


class BancoNoDisponible(Exception):
    """El banco no respondió a tiempo."""


# Probabilidad de que una consulta falle y rango de demora en segundos.
PROB_FALLA = float(os.environ.get("BANCO_PROB_FALLA", "0.25"))
DEMORA_MIN = float(os.environ.get("BANCO_DEMORA_MIN", "0.1"))
DEMORA_MAX = float(os.environ.get("BANCO_DEMORA_MAX", "1.2"))

# Transferencias que el banco reporta como devueltas al ordenante.
_DEVUELTAS = {"20261017BANORTE00000418827"}


def consultar_transferencia(clave_rastreo: str) -> dict:
    time.sleep(random.uniform(DEMORA_MIN, DEMORA_MAX))
    if random.random() < PROB_FALLA:
        raise BancoNoDisponible("El banco no respondió (tiempo de espera agotado)")
    estatus = "DEVUELTA" if clave_rastreo in _DEVUELTAS else "LIQUIDADA"
    return {"clave_rastreo": clave_rastreo, "estatus": estatus}
