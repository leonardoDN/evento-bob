from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app import pac_simulado
from app.db import conexion
from app.pac_simulado import PacNoDisponible
from app.timbrado import ErrorTimbrado, timbrar_factura

MOTIVOS = {
    "01": "Comprobante emitido con errores con relación",
    "02": "Comprobante emitido con errores sin relación",
    "03": "No se llevó a cabo la operación",
    "04": "Operación nominativa relacionada en una factura global",
}


class SolicitudCancelacion(BaseModel):
    motivo: str

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


@router.post("/{factura_id}/cancelar")
def cancelar(factura_id: int, solicitud: SolicitudCancelacion):
    motivo = solicitud.motivo.strip()
    if motivo not in "01020304":
        raise HTTPException(422, "Motivo de cancelación inválido")

    with conexion() as con:
        factura = con.execute(
            "SELECT f.*, p.total, p.cliente_id FROM facturas f JOIN pedidos p ON p.id = f.pedido_id "
            "WHERE f.id = ?",
            (factura_id,),
        ).fetchone()
        if factura is None:
            raise HTTPException(404, "Factura no encontrada")
        if factura["estado"] != "timbrada":
            raise HTTPException(409, "Solo se pueden cancelar facturas timbradas")
        con.execute("UPDATE clientes SET saldo = saldo - ? WHERE id = ?", (factura["total"], factura["cliente_id"]))

    try:
        respuesta = pac_simulado.solicitar_cancelacion(factura["uuid"], motivo)
    except PacNoDisponible as e:
        raise HTTPException(503, str(e))

    with conexion() as con:
        con.execute(
            f"UPDATE facturas SET estado = 'cancelada', motivo_cancelacion = '{motivo}', "
            f"fecha_cancelacion = '{respuesta['fecha']}' WHERE id = {factura_id}"
        )
    return {"factura_id": factura_id, "estado": "cancelada", "motivo": MOTIVOS.get(motivo, motivo)}
