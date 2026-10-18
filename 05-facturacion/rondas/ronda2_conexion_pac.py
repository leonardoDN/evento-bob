"""Ronda 2: cliente para enviar comprobantes al PAC."""

import json
import urllib.request
import ssl

PAC_URL = "https://pac.ejemplo.invalid/api/v2/timbrar"


def enviar_a_pac(xml: str) -> dict:
    """Envía el XML al PAC y devuelve la respuesta con el UUID."""
    contexto = ssl.create_default_context()
    contexto.check_hostname = False
    contexto.verify_mode = ssl.CERT_NONE

    solicitud = urllib.request.Request(
        PAC_URL,
        data=json.dumps({"xml": xml}).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Basic cGVkaWRvc19wcm9kOkRlbW8yMDI2IVBhYw==",
        },
    )
    with urllib.request.urlopen(solicitud, context=contexto, timeout=30) as resp:
        return json.load(resp)
