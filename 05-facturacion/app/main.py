"""Punto de entrada de la aplicación de pedidos y facturación."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app import db
from app.rutas import clientes, facturas, pedidos, productos

ESTATICOS = Path(__file__).resolve().parent.parent / "static"

db.inicializar()

app = FastAPI(title="Pedidos y facturación")
app.include_router(clientes.router)
app.include_router(productos.router)
app.include_router(pedidos.router)
app.include_router(facturas.router)
app.mount("/static", StaticFiles(directory=ESTATICOS), name="static")


@app.get("/", include_in_schema=False)
def inicio():
    return FileResponse(ESTATICOS / "index.html")
