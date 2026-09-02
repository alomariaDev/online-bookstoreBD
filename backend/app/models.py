from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, DateTime, ForeignKey, Numeric, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class Cliente(Base):
    __tablename__ = "clientes"

    cliente_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    telefono: Mapped[str | None] = mapped_column(String(20))
    ciudad: Mapped[str | None] = mapped_column(String(80))
    pais: Mapped[str | None] = mapped_column(String(80))
    creado_en: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.current_timestamp())
    pedidos: Mapped[list["Pedido"]] = relationship(back_populates="cliente")


class Libro(Base):
    __tablename__ = "libros"

    libro_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    titulo: Mapped[str] = mapped_column(String(200))
    autor: Mapped[str] = mapped_column(String(150))
    genero: Mapped[str | None] = mapped_column(String(80))
    anio_publicacion: Mapped[int | None]
    precio: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    stock: Mapped[int]
    detalles: Mapped[list["DetallePedido"]] = relationship(back_populates="libro")


class Pedido(Base):
    __tablename__ = "pedidos"

    pedido_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.cliente_id"))
    fecha_pedido: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.current_timestamp())
    estado: Mapped[str] = mapped_column(String(20))
    cliente: Mapped[Cliente] = relationship(back_populates="pedidos")
    detalles: Mapped[list["DetallePedido"]] = relationship(back_populates="pedido", cascade="all, delete-orphan")


class DetallePedido(Base):
    __tablename__ = "detalle_pedido"
    __table_args__ = (UniqueConstraint("pedido_id", "libro_id"),)

    detalle_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    pedido_id: Mapped[int] = mapped_column(ForeignKey("pedidos.pedido_id", ondelete="CASCADE"))
    libro_id: Mapped[int] = mapped_column(ForeignKey("libros.libro_id"))
    cantidad: Mapped[int]
    precio_unitario: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    pedido: Mapped[Pedido] = relationship(back_populates="detalles")
    libro: Mapped[Libro] = relationship(back_populates="detalles")
