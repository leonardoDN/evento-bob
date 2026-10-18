"""Punto de entrada de la aplicación de órdenes de servicio."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app import db
from app.rutas import catalogos, equipos, ordenes

ESTATICOS = Path(__file__).resolve().parent.parent / "static"

db.inicializar()

app = FastAPI(title="Órdenes de servicio")
app.include_router(catalogos.router)
app.include_router(equipos.router)
app.include_router(ordenes.router)
app.mount("/static", StaticFiles(directory=ESTATICOS), name="static")


@app.get("/", include_in_schema=False)
def inicio():
    return FileResponse(ESTATICOS / "index.html")
