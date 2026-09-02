from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class LibroOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    libro_id: int
    titulo: str
    autor: str
    genero: str | None
    anio_publicacion: int | None
    precio: Decimal
    stock: int


class ClienteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    cliente_id: int
    nombre: str
    email: str
    telefono: str | None
    ciudad: str | None
    pais: str | None
    creado_en: datetime


class ItemPedidoIn(BaseModel):
    libro_id: int
    cantidad: int = Field(gt=0, le=100)


class PedidoIn(BaseModel):
    cliente_id: int
    items: list[ItemPedidoIn] = Field(min_length=1)


class PedidoItemOut(BaseModel):
    libro_id: int
    titulo: str
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal


class PedidoOut(BaseModel):
    pedido_id: int
    cliente_id: int
    estado: str
    fecha_pedido: datetime
    total: Decimal
    items: list[PedidoItemOut]
