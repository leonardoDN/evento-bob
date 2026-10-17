"""Acceso a la base de datos SQLite del sistema de pedidos."""

import os
import sqlite3
from contextlib import contextmanager
from decimal import Decimal
from pathlib import Path

sqlite3.register_adapter(Decimal, str)

RUTA_BD = Path(os.environ.get("PEDIDOS_BD", Path(__file__).resolve().parent.parent / "datos" / "pedidos.db"))

ESQUEMA = """
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY,
    rfc TEXT NOT NULL UNIQUE,
    razon_social TEXT NOT NULL,
    codigo_postal TEXT NOT NULL,
    uso_cfdi TEXT NOT NULL DEFAULT 'G03',
    saldo NUMERIC NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS productos (
    sku TEXT PRIMARY KEY,
    descripcion TEXT NOT NULL,
    precio NUMERIC NOT NULL,
    clave_sat TEXT NOT NULL,
    unidad_sat TEXT NOT NULL DEFAULT 'H87'
);

CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY,
    cliente_id INTEGER NOT NULL REFERENCES clientes(id),
    fecha TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    estado TEXT NOT NULL DEFAULT 'capturado',
    subtotal NUMERIC NOT NULL DEFAULT 0,
    iva NUMERIC NOT NULL DEFAULT 0,
    total NUMERIC NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS renglones (
    id INTEGER PRIMARY KEY,
    pedido_id INTEGER NOT NULL REFERENCES pedidos(id),
    sku TEXT NOT NULL REFERENCES productos(sku),
    cantidad INTEGER NOT NULL,
    precio NUMERIC NOT NULL,
    importe NUMERIC NOT NULL
);

CREATE TABLE IF NOT EXISTS facturas (
    id INTEGER PRIMARY KEY,
    pedido_id INTEGER NOT NULL UNIQUE REFERENCES pedidos(id),
    serie TEXT NOT NULL DEFAULT 'A',
    folio INTEGER NOT NULL,
    uuid TEXT,
    fecha_timbrado TEXT,
    estado TEXT NOT NULL DEFAULT 'pendiente',
    motivo_cancelacion TEXT,
    fecha_cancelacion TEXT
);
"""

SEMILLA = """
INSERT INTO clientes (rfc, razon_social, codigo_postal, uso_cfdi, saldo) VALUES
    ('DNO920315AB1', 'Distribuidora del Noreste', '64000', 'G01', 18500.00),
    ('FHM031122KL7', 'Ferretería Hermanos Medina', '44100', 'G03', 0),
    ('CPA101010QW3', 'Constructora del Pacífico', '82000', 'G03', 152000.00),
    ('MTE850707TT2', 'Materiales Técnicos del Bajío', '37000', 'G01', 4200.00);

INSERT INTO productos (sku, descripcion, precio, clave_sat, unidad_sat) VALUES
    ('TUB-PVC-4', 'Tubo PVC sanitario 4 pulgadas, 6 m', 389.00, '40142000', 'H87'),
    ('CEM-GRS-50', 'Cemento gris, bulto 50 kg', 245.50, '30111601', 'XBG'),
    ('VAR-38-12', 'Varilla corrugada 3/8, 12 m', 162.90, '30102200', 'H87'),
    ('CAB-THW-12', 'Cable THW calibre 12, rollo 100 m', 1189.00, '26121600', 'XRO'),
    ('PIN-VIN-19', 'Pintura vinílica blanca, cubeta 19 L', 1450.00, '31211500', 'XBJ');
"""


def inicializar(ruta: Path = RUTA_BD) -> None:
    """Crea las tablas y, si la base está vacía, carga los datos de ejemplo."""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(ruta) as con:
        con.executescript(ESQUEMA)
        if con.execute("SELECT COUNT(*) FROM clientes").fetchone()[0] == 0:
            con.executescript(SEMILLA)


@contextmanager
def conexion():
    con = sqlite3.connect(RUTA_BD)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    try:
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()
