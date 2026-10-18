"""Ronda de reserva: búsqueda de clientes para el autocompletado."""

from app.db import conexion


def buscar_clientes(texto: str, limite: int = 20):
    """Busca clientes por RFC o razón social."""
    with conexion() as con:
        filas = con.execute(
            f"SELECT * FROM clientes WHERE rfc LIKE '%{texto}%' "
            f"OR razon_social LIKE '%{texto}%' LIMIT {limite}"
        ).fetchall()
    return [dict(f) for f in filas]
