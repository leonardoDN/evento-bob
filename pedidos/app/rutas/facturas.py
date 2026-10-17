from fastapi import APIRouter, HTTPException

from app.db import conexion
from app.pac_simulado import PacNoDisponible
from app.timbrado import ErrorTimbrado, timbrar_factura

router = APIRouter(prefix="/api/facturas", tags=["facturas"])


@router.get("")
def listar_facturas():
    with conexion() as con:
        filas = con.execute(
            "SELECT f.*, p.total, c.razon_social, c.rfc FROM facturas f "
            "JOIN pedidos p ON p.id = f.pedido_id JOIN clientes c ON c.id = p.cliente_id "
            "ORDER BY f.id DESC"
        )
        return [dict(f) for f in filas]


@router.post("/desde-pedido/{pedido_id}", status_code=201)
def facturar_pedido(pedido_id: int):
    with conexion() as con:
        pedido = con.execute("SELECT * FROM pedidos WHERE id = ?", (pedido_id,)).fetchone()
        if pedido is None:
            raise HTTPException(404, "Pedido no encontrado")
        existente = con.execute("SELECT id FROM facturas WHERE pedido_id = ?", (pedido_id,)).fetchone()
        if existente:
            factura_id = existente["id"]
        else:
            folio = con.execute("SELECT COALESCE(MAX(folio), 1000) + 1 FROM facturas").fetchone()[0]
            factura_id = con.execute(
                "INSERT INTO facturas (pedido_id, folio) VALUES (?, ?)", (pedido_id, folio)
            ).lastrowid
    return timbrar(factura_id)


@router.post("/{factura_id}/timbrar")
def timbrar(factura_id: int):
    try:
        return timbrar_factura(factura_id)
    except ErrorTimbrado as e:
        raise HTTPException(409, str(e))
    except PacNoDisponible as e:
        raise HTTPException(503, str(e))
