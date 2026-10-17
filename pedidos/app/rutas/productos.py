from fastapi import APIRouter

from app.db import conexion

router = APIRouter(prefix="/api/productos", tags=["productos"])


@router.get("")
def listar_productos():
    with conexion() as con:
        return [dict(p) for p in con.execute("SELECT * FROM productos ORDER BY descripcion")]
