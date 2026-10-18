import sqlite3

from fastapi import APIRouter, HTTPException

from app.db import conexion
from app.modelos import EquipoNuevo

router = APIRouter(prefix="/api/equipos", tags=["equipos"])


@router.get("")
def listar_equipos(cliente_id: int | None = None):
    consulta = (
        "SELECT e.*, c.razon_social, c.planta FROM equipos e JOIN clientes c ON c.id = e.cliente_id"
    )
    with conexion() as con:
        if cliente_id is None:
            filas = con.execute(consulta + " ORDER BY c.razon_social, e.numero_serie")
        else:
            filas = con.execute(consulta + " WHERE e.cliente_id = ? ORDER BY e.numero_serie", (cliente_id,))
        return [dict(e) for e in filas]


@router.get("/{equipo_id}")
def obtener_equipo(equipo_id: int):
    with conexion() as con:
        equipo = con.execute(
            "SELECT e.*, c.razon_social, c.planta FROM equipos e JOIN clientes c ON c.id = e.cliente_id "
            "WHERE e.id = ?",
            (equipo_id,),
        ).fetchone()
        if equipo is None:
            raise HTTPException(404, "Equipo no encontrado")
        historial = con.execute(
            "SELECT id, tipo, estado, fecha_apertura, fecha_cierre, falla_reportada, total "
            "FROM ordenes WHERE equipo_id = ? ORDER BY fecha_apertura DESC",
            (equipo_id,),
        ).fetchall()
    return {**dict(equipo), "historial": [dict(o) for o in historial]}


@router.post("", status_code=201)
def registrar_equipo(datos: EquipoNuevo):
    try:
        with conexion() as con:
            if con.execute("SELECT 1 FROM clientes WHERE id = ?", (datos.cliente_id,)).fetchone() is None:
                raise HTTPException(404, "Cliente no encontrado")
            cur = con.execute(
                "INSERT INTO equipos (cliente_id, numero_serie, tipo, marca, modelo, ubicacion, fecha_instalacion) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (datos.cliente_id, datos.numero_serie.upper(), datos.tipo, datos.marca, datos.modelo,
                 datos.ubicacion, datos.fecha_instalacion),
            )
            return {"id": cur.lastrowid}
    except sqlite3.IntegrityError:
        raise HTTPException(409, "Ya existe un equipo con ese número de serie")
