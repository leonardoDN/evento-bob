"""Esquemas de entrada y salida de la API."""

from pydantic import BaseModel, Field


class ClienteNuevo(BaseModel):
    rfc: str = Field(min_length=12, max_length=13)
    razon_social: str = Field(min_length=1)
    codigo_postal: str = Field(pattern=r"^\d{5}$")
    uso_cfdi: str = "G03"


class RenglonNuevo(BaseModel):
    sku: str
    cantidad: int = Field(gt=0)


class PedidoNuevo(BaseModel):
    cliente_id: int
    renglones: list[RenglonNuevo] = Field(min_length=1)
