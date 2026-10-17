import sqlite3

from fastapi import APIRouter, HTTPException

from app.db import conexion
from app.modelos import ClienteNuevo

router = APIRouter(prefix="/api/clientes", tags=["clientes"])


@router.get("")
def listar_clientes():
    with conexion() as con:
        return [dict(c) for c in con.execute("SELECT * FROM clientes ORDER BY razon_social")]


@router.get("/{cliente_id}")
def obtener_cliente(cliente_id: int):
    with conexion() as con:
        cliente = con.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,)).fetchone()
    if cliente is None:
        raise HTTPException(404, "Cliente no encontrado")
    return dict(cliente)


@router.post("", status_code=201)
def crear_cliente(datos: ClienteNuevo):
    try:
        with conexion() as con:
            cur = con.execute(
                "INSERT INTO clientes (rfc, razon_social, codigo_postal, uso_cfdi) VALUES (?, ?, ?, ?)",
                (datos.rfc.upper(), datos.razon_social, datos.codigo_postal, datos.uso_cfdi),
            )
            return {"id": cur.lastrowid}
    except sqlite3.IntegrityError:
        raise HTTPException(409, "Ya existe un cliente con ese RFC")
