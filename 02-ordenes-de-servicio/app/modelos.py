"""Esquemas de entrada y salida de la API."""

from typing import Literal

from pydantic import BaseModel, Field


class EquipoNuevo(BaseModel):
    cliente_id: int
    numero_serie: str = Field(min_length=1)
    tipo: Literal["bomba", "compresor", "caldera", "motor"]
    marca: str = Field(min_length=1)
    modelo: str = Field(min_length=1)
    ubicacion: str = Field(min_length=1)
    fecha_instalacion: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")


class OrdenNueva(BaseModel):
    equipo_id: int
    tipo: Literal["correctiva", "preventiva"]
    falla_reportada: str = Field(min_length=1)


class Asignacion(BaseModel):
    tecnico_id: int


class RefaccionUsada(BaseModel):
    clave: str
    cantidad: int = Field(gt=0)


class Cierre(BaseModel):
    diagnostico: str = Field(min_length=1)
    horas_mano_obra: float = Field(gt=0, le=200)
