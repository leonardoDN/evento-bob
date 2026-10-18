from fastapi import APIRouter, HTTPException

from app.costos import costo_orden, importe_refaccion
from app.db import conexion
from app.modelos import Asignacion, Cierre, OrdenNueva, RefaccionUsada

router = APIRouter(prefix="/api/ordenes", tags=["órdenes"])

CONSULTA_ORDEN = (
    "SELECT o.*, e.numero_serie, e.tipo AS tipo_equipo, e.modelo, e.ubicacion, "
    "c.razon_social, c.planta, t.nombre AS tecnico FROM ordenes o "
    "JOIN equipos e ON e.id = o.equipo_id JOIN clientes c ON c.id = e.cliente_id "
    "LEFT JOIN tecnicos t ON t.id = o.tecnico_id"
)


def _orden_abierta(con, orden_id: int):
    orden = con.execute("SELECT * FROM ordenes WHERE id = ?", (orden_id,)).fetchone()
    if orden is None:
        raise HTTPException(404, "Orden no encontrada")
    if orden["estado"] == "cerrada":
        raise HTTPException(409, "La orden ya está cerrada")
    return orden


@router.get("")
def listar_ordenes(estado: str | None = None):
    with conexion() as con:
        if estado is None:
            filas = con.execute(CONSULTA_ORDEN + " ORDER BY o.id DESC")
        else:
            filas = con.execute(CONSULTA_ORDEN + " WHERE o.estado = ? ORDER BY o.id DESC", (estado,))
        return [dict(o) for o in filas]


@router.get("/{orden_id}")
def obtener_orden(orden_id: int):
    with conexion() as con:
        orden = con.execute(CONSULTA_ORDEN + " WHERE o.id = ?", (orden_id,)).fetchone()
        if orden is None:
            raise HTTPException(404, "Orden no encontrada")
        refacciones = con.execute(
            "SELECT orf.*, r.descripcion FROM orden_refacciones orf "
            "JOIN refacciones r ON r.clave = orf.clave WHERE orf.orden_id = ?",
            (orden_id,),
        ).fetchall()
    return {**dict(orden), "refacciones": [dict(r) for r in refacciones]}


@router.post("", status_code=201)
def abrir_orden(datos: OrdenNueva):
    with conexion() as con:
        if con.execute("SELECT 1 FROM equipos WHERE id = ?", (datos.equipo_id,)).fetchone() is None:
            raise HTTPException(404, "Equipo no encontrado")
        cur = con.execute(
            "INSERT INTO ordenes (equipo_id, tipo, falla_reportada) VALUES (?, ?, ?)",
            (datos.equipo_id, datos.tipo, datos.falla_reportada),
        )
    return {"id": cur.lastrowid, "estado": "abierta"}


@router.post("/{orden_id}/asignar")
def asignar_tecnico(orden_id: int, datos: Asignacion):
    with conexion() as con:
        _orden_abierta(con, orden_id)
        if con.execute("SELECT 1 FROM tecnicos WHERE id = ?", (datos.tecnico_id,)).fetchone() is None:
            raise HTTPException(404, "Técnico no encontrado")
        con.execute(
            "UPDATE ordenes SET tecnico_id = ?, estado = 'en_proceso' WHERE id = ?", (datos.tecnico_id, orden_id)
        )
    return {"id": orden_id, "estado": "en_proceso"}


@router.post("/{orden_id}/refacciones", status_code=201)
def agregar_refaccion(orden_id: int, datos: RefaccionUsada):
    with conexion() as con:
        _orden_abierta(con, orden_id)
        refaccion = con.execute("SELECT * FROM refacciones WHERE clave = ?", (datos.clave,)).fetchone()
        if refaccion is None:
            raise HTTPException(404, f"No existe la refacción {datos.clave}")
        if refaccion["existencias"] < datos.cantidad:
            raise HTTPException(422, f"Solo hay {refaccion['existencias']} en almacén de {datos.clave}")
        importe = importe_refaccion(refaccion["precio"], datos.cantidad)
        con.execute(
            "INSERT INTO orden_refacciones (orden_id, clave, cantidad, precio, importe) VALUES (?, ?, ?, ?, ?)",
            (orden_id, datos.clave, datos.cantidad, refaccion["precio"], importe),
        )
        con.execute("UPDATE refacciones SET existencias = existencias - ? WHERE clave = ?", (datos.cantidad, datos.clave))
    return {"orden_id": orden_id, "clave": datos.clave, "importe": importe}


@router.post("/{orden_id}/cerrar")
def cerrar_orden(orden_id: int, datos: Cierre):
    with conexion() as con:
        orden = _orden_abierta(con, orden_id)
        if orden["tecnico_id"] is None:
            raise HTTPException(409, "Asigna un técnico antes de cerrar la orden")
        importes = [r["importe"] for r in con.execute(
            "SELECT importe FROM orden_refacciones WHERE orden_id = ?", (orden_id,)
        )]
        costo = costo_orden(datos.horas_mano_obra, importes)
        con.execute(
            "UPDATE ordenes SET estado = 'cerrada', fecha_cierre = datetime('now', 'localtime'), "
            "diagnostico = ?, horas_mano_obra = ?, costo_mano_obra = ?, costo_refacciones = ?, "
            "subtotal = ?, iva = ?, total = ? WHERE id = ?",
            (datos.diagnostico, datos.horas_mano_obra, costo["costo_mano_obra"], costo["costo_refacciones"],
             costo["subtotal"], costo["iva"], costo["total"], orden_id),
        )
    return {"id": orden_id, "estado": "cerrada", **costo}
