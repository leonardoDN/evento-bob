"""Acceso a la base de datos SQLite del sistema de órdenes de servicio."""

import os
import sqlite3
from contextlib import contextmanager
from decimal import Decimal
from pathlib import Path

sqlite3.register_adapter(Decimal, str)

RUTA_BD = Path(os.environ.get("ORDENES_BD", Path(__file__).resolve().parent.parent / "datos" / "ordenes.db"))

ESQUEMA = """
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY,
    rfc TEXT NOT NULL UNIQUE,
    razon_social TEXT NOT NULL,
    planta TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS equipos (
    id INTEGER PRIMARY KEY,
    cliente_id INTEGER NOT NULL REFERENCES clientes(id),
    numero_serie TEXT NOT NULL UNIQUE,
    tipo TEXT NOT NULL CHECK (tipo IN ('bomba', 'compresor', 'caldera', 'motor')),
    marca TEXT NOT NULL,
    modelo TEXT NOT NULL,
    ubicacion TEXT NOT NULL,
    fecha_instalacion TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tecnicos (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    especialidad TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS refacciones (
    clave TEXT PRIMARY KEY,
    descripcion TEXT NOT NULL,
    precio NUMERIC NOT NULL,
    existencias INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS ordenes (
    id INTEGER PRIMARY KEY,
    equipo_id INTEGER NOT NULL REFERENCES equipos(id),
    tecnico_id INTEGER REFERENCES tecnicos(id),
    tipo TEXT NOT NULL CHECK (tipo IN ('correctiva', 'preventiva')),
    estado TEXT NOT NULL DEFAULT 'abierta',
    fecha_apertura TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    fecha_cierre TEXT,
    falla_reportada TEXT NOT NULL,
    diagnostico TEXT,
    horas_mano_obra NUMERIC,
    costo_mano_obra NUMERIC NOT NULL DEFAULT 0,
    costo_refacciones NUMERIC NOT NULL DEFAULT 0,
    subtotal NUMERIC NOT NULL DEFAULT 0,
    iva NUMERIC NOT NULL DEFAULT 0,
    total NUMERIC NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS orden_refacciones (
    id INTEGER PRIMARY KEY,
    orden_id INTEGER NOT NULL REFERENCES ordenes(id),
    clave TEXT NOT NULL REFERENCES refacciones(clave),
    cantidad INTEGER NOT NULL,
    precio NUMERIC NOT NULL,
    importe NUMERIC NOT NULL
);
"""

SEMILLA = """
INSERT INTO clientes (rfc, razon_social, planta) VALUES
    ('EVA990301RT5', 'Embotelladora del Valle', 'Toluca, Edo. de México'),
    ('PNO050617HJ2', 'Papelera del Norte', 'Apodaca, Nuevo León'),
    ('QIG120904PL8', 'Química Industrial del Golfo', 'Coatzacoalcos, Veracruz'),
    ('ALH080215MN4', 'Alimentos La Huerta', 'Celaya, Guanajuato');

INSERT INTO equipos (cliente_id, numero_serie, tipo, marca, modelo, ubicacion, fecha_instalacion) VALUES
    (1, 'BC-2019-0441', 'bomba', 'Hidromex', 'HC-150 centrífuga', 'Línea 2, agua de proceso', '2019-03-12'),
    (1, 'CT-2021-1187', 'compresor', 'Aerotec', 'AT-75 de tornillo', 'Cuarto de compresores', '2021-08-02'),
    (2, 'CL-2016-0093', 'caldera', 'Termoindustrial', 'TP-300 pirotubular', 'Casa de máquinas', '2016-11-20'),
    (2, 'MT-2020-5520', 'motor', 'Electromotriz', 'EM-75 HP trifásico', 'Molino 1', '2020-01-15'),
    (3, 'BC-2018-0310', 'bomba', 'Hidromex', 'HC-200 centrífuga', 'Transferencia de ácido', '2018-06-04'),
    (3, 'CR-2015-0777', 'compresor', 'Aerotec', 'AR-40 reciprocante', 'Planta de aire', '2015-09-30'),
    (4, 'CL-2022-0158', 'caldera', 'Termoindustrial', 'TP-150 pirotubular', 'Cocción', '2022-02-28');

INSERT INTO tecnicos (nombre, especialidad) VALUES
    ('Gabriela Ruiz', 'Bombas y sellos mecánicos'),
    ('Héctor Villalobos', 'Compresores'),
    ('Ingrid Paredes', 'Calderas y motores');

INSERT INTO refacciones (clave, descripcion, precio, existencias) VALUES
    ('SM-45', 'Sello mecánico 45 mm', 3850.00, 6),
    ('ROD-6310', 'Rodamiento 6310', 1240.00, 14),
    ('FIL-AC-12', 'Filtro de aceite para compresor', 980.00, 9),
    ('KIT-VAL-R', 'Kit de válvulas para compresor reciprocante', 6700.00, 2),
    ('EMP-GRAF', 'Empaque de grafito', 450.00, 25),
    ('TERM-K', 'Termopar tipo K', 720.00, 0);

INSERT INTO ordenes (equipo_id, tecnico_id, tipo, estado, fecha_apertura, falla_reportada) VALUES
    (1, 1, 'correctiva', 'en_proceso', '2026-10-14 08:20:00', 'Fuga por el sello, goteo constante'),
    (6, NULL, 'correctiva', 'abierta', '2026-10-16 17:45:00', 'No alcanza la presión de trabajo'),
    (3, NULL, 'preventiva', 'abierta', '2026-10-17 09:00:00', 'Mantenimiento semestral');

INSERT INTO orden_refacciones (orden_id, clave, cantidad, precio, importe) VALUES
    (1, 'SM-45', 1, 3850.00, 3850.00);
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
