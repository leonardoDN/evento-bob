"""Cotización de envíos por peso cobrable y zona de destino."""

import math
from decimal import ROUND_HALF_UP, Decimal

# Divisor volumétrico de las paqueterías: centímetros cúbicos por kilogramo.
FACTOR_VOLUMETRICO = 5000
PESO_MAXIMO_KG = 70

# Zona por los dos primeros dígitos del código postal de destino.
ZONAS = {
    1: range(1, 17),     # Ciudad de México
    2: range(50, 63),    # Centro: Estado de México, Morelos, Puebla, Querétaro, Hidalgo, Tlaxcala
    3: range(64, 68),    # Nuevo León
    4: range(77, 98),    # Sureste y península
    5: range(21, 24),    # Baja California y Baja California Sur
}
ZONA_RESTO_DEL_PAIS = 6

# Por zona: (precio de los primeros 5 kg, precio por kg adicional).
TARIFAS = {
    1: (Decimal("95.00"), Decimal("12.00")),
    2: (Decimal("135.00"), Decimal("16.50")),
    3: (Decimal("165.00"), Decimal("19.00")),
    4: (Decimal("189.00"), Decimal("23.50")),
    5: (Decimal("245.00"), Decimal("31.00")),
    6: (Decimal("175.00"), Decimal("21.00")),
}
KG_INCLUIDOS = 5
CENTAVO = Decimal("0.01")


class EnvioInvalido(ValueError):
    """El paquete no se puede cotizar."""


def peso_volumetrico(largo_cm: float, ancho_cm: float, alto_cm: float) -> float:
    """Calcula el peso volumétrico en kilogramos.

    Args:
        largo_cm: largo del paquete en centímetros.
        ancho_cm: ancho del paquete en centímetros.
        alto_cm: alto del paquete en centímetros.

    Returns:
        Peso volumétrico en kilogramos, sin redondear.
    """
    return largo_cm * ancho_cm * alto_cm / FACTOR_VOLUMETRICO


def peso_cobrable(peso_real_kg: float, largo_cm: float, ancho_cm: float, alto_cm: float) -> int:
    """Determina el peso que se cobra: el mayor entre el real y el volumétrico.

    Args:
        peso_real_kg: peso en báscula.
        largo_cm: largo del paquete en centímetros.
        ancho_cm: ancho del paquete en centímetros.
        alto_cm: alto del paquete en centímetros.

    Returns:
        Kilogramos cobrables, redondeados hacia arriba al kilo entero.
    """
    return math.ceil(max(peso_real_kg, peso_volumetrico(largo_cm, ancho_cm, alto_cm)))


def zona_destino(codigo_postal: str) -> int:
    """Asigna la zona tarifaria según el código postal de destino.

    Args:
        codigo_postal: código postal de cinco dígitos.

    Returns:
        Número de zona, del 1 al 6.

    Raises:
        EnvioInvalido: si el código postal no tiene cinco dígitos.
    """
    if len(codigo_postal) != 5 or not codigo_postal.isdigit():
        raise EnvioInvalido(f"Código postal inválido: {codigo_postal!r}")
    prefijo = int(codigo_postal[:2])
    for zona, prefijos in ZONAS.items():
        if prefijo in prefijos:
            return zona
    return ZONA_RESTO_DEL_PAIS


def cotizar(codigo_postal: str, peso_real_kg: float, largo_cm: float, ancho_cm: float, alto_cm: float) -> dict:
    """Cotiza un envío nacional.

    Args:
        codigo_postal: código postal de destino.
        peso_real_kg: peso en báscula.
        largo_cm: largo del paquete en centímetros.
        ancho_cm: ancho del paquete en centímetros.
        alto_cm: alto del paquete en centímetros.

    Returns:
        Diccionario con zona, kilogramos cobrables y precio sin IVA.

    Raises:
        EnvioInvalido: si el código postal es inválido o el paquete excede el peso máximo.
    """
    kilos = peso_cobrable(peso_real_kg, largo_cm, ancho_cm, alto_cm)
    if kilos > PESO_MAXIMO_KG:
        raise EnvioInvalido(f"El paquete pesa {kilos} kg cobrables; el máximo es {PESO_MAXIMO_KG}")
    zona = zona_destino(codigo_postal)
    base, adicional = TARIFAS[zona]
    precio = base + adicional * max(kilos - KG_INCLUIDOS, 0)
    return {"zona": zona, "kilos_cobrables": kilos, "precio": precio.quantize(CENTAVO, rounding=ROUND_HALF_UP)}
