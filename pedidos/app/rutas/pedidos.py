from fastapi import APIRouter, HTTPException

from app.calculo import importe_renglon, totales
from app.db import conexion
from app.modelos import PedidoNuevo

router = APIRouter(prefix="/api/pedidos", tags=["pedidos"])


@router.get("")
def listar_pedidos():
    with conexion() as con:
        filas = con.execute(
            "SELECT p.*, c.razon_social FROM pedidos p JOIN clientes c ON c.id = p.cliente_id "
            "ORDER BY p.id DESC"
        )
        return [dict(f) for f in filas]


@router.get("/{pedido_id}")
def obtener_pedido(pedido_id: int):
    with conexion() as con:
        pedido = con.execute("SELECT * FROM pedidos WHERE id = ?", (pedido_id,)).fetchone()
        if pedido is None:
            raise HTTPException(404, "Pedido no encontrado")
        renglones = con.execute(
            "SELECT r.*, p.descripcion FROM renglones r JOIN productos p ON p.sku = r.sku "
            "WHERE r.pedido_id = ?",
            (pedido_id,),
        ).fetchall()
    return {**dict(pedido), "renglones": [dict(r) for r in renglones]}


@router.post("", status_code=201)
def crear_pedido(datos: PedidoNuevo):
    with conexion() as con:
        if con.execute("SELECT 1 FROM clientes WHERE id = ?", (datos.cliente_id,)).fetchone() is None:
            raise HTTPException(404, "Cliente no encontrado")

        renglones = []
        for r in datos.renglones:
            producto = con.execute("SELECT * FROM productos WHERE sku = ?", (r.sku,)).fetchone()
            if producto is None:
                raise HTTPException(422, f"No existe el producto {r.sku}")
            renglones.append((r.sku, r.cantidad, producto["precio"], importe_renglon(producto["precio"], r.cantidad)))

        t = totales([importe for *_, importe in renglones])
        cur = con.execute(
            "INSERT INTO pedidos (cliente_id, subtotal, iva, total) VALUES (?, ?, ?, ?)",
            (datos.cliente_id, t["subtotal"], t["iva"], t["total"]),
        )
        pedido_id = cur.lastrowid
        con.executemany(
            "INSERT INTO renglones (pedido_id, sku, cantidad, precio, importe) VALUES (?, ?, ?, ?, ?)",
            [(pedido_id, *r) for r in renglones],
        )
        con.execute("UPDATE clientes SET saldo = saldo + ? WHERE id = ?", (t["total"], datos.cliente_id))
    return {"id": pedido_id, **t}
