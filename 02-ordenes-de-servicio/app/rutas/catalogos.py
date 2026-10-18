from fastapi import APIRouter

from app.db import conexion

router = APIRouter(prefix="/api", tags=["catálogos"])


@router.get("/clientes")
def listar_clientes():
    with conexion() as con:
        return [dict(c) for c in con.execute("SELECT * FROM clientes ORDER BY razon_social")]


@router.get("/tecnicos")
def listar_tecnicos():
    with conexion() as con:
        return [dict(t) for t in con.execute("SELECT * FROM tecnicos ORDER BY nombre")]


@router.get("/refacciones")
def listar_refacciones():
    with conexion() as con:
        return [dict(r) for r in con.execute("SELECT * FROM refacciones ORDER BY descripcion")]
