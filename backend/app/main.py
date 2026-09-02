from decimal import Decimal
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from .db import SessionLocal
from .models import Cliente, DetallePedido, Libro, Pedido
from .schemas import ClienteOut, LibroOut, PedidoIn, PedidoOut

app = FastAPI(title="Online Bookstore API", version="1.0.0")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]


@app.get("/health", tags=["Sistema"])
def health(db: DbSession):
    db.execute(select(1))
    return {"status": "ok", "database": "online_bookstorebd"}


@app.get("/api/v1/libros", response_model=list[LibroOut], tags=["Libros"])
def listar_libros(
    db: DbSession,
    genero: str | None = None,
    autor: str | None = None,
    disponible: bool = False,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    query = select(Libro).order_by(Libro.libro_id).limit(limit).offset(offset)
    if genero:
        query = query.where(Libro.genero.ilike(f"%{genero}%"))
    if autor:
        query = query.where(Libro.autor.ilike(f"%{autor}%"))
    if disponible:
        query = query.where(Libro.stock > 0)
    return db.scalars(query).all()


@app.get("/api/v1/libros/{libro_id}", response_model=LibroOut, tags=["Libros"])
def obtener_libro(libro_id: int, db: DbSession):
    libro = db.get(Libro, libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro


@app.get("/api/v1/clientes/{cliente_id}", response_model=ClienteOut, tags=["Clientes"])
def obtener_cliente(cliente_id: int, db: DbSession):
    cliente = db.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@app.post("/api/v1/pedidos", response_model=PedidoOut, status_code=status.HTTP_201_CREATED, tags=["Pedidos"])
def crear_pedido(payload: PedidoIn, db: DbSession):
    if len({item.libro_id for item in payload.items}) != len(payload.items):
        raise HTTPException(status_code=422, detail="No repitas libros dentro del pedido")

    try:
        cliente = db.get(Cliente, payload.cliente_id)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        pedido = Pedido(cliente_id=cliente.cliente_id, estado="pendiente")
        db.add(pedido)
        db.flush()
        detalles = []

        for item in payload.items:
            libro = db.scalar(select(Libro).where(Libro.libro_id == item.libro_id).with_for_update())
            if not libro:
                raise HTTPException(status_code=404, detail=f"Libro {item.libro_id} no encontrado")
            if libro.stock < item.cantidad:
                raise HTTPException(status_code=409, detail=f"Stock insuficiente para el libro {item.libro_id}")
            precio = libro.precio
            libro.stock -= item.cantidad
            detalles.append(DetallePedido(
                pedido_id=pedido.pedido_id,
                libro_id=libro.libro_id,
                cantidad=item.cantidad,
                precio_unitario=precio,
                libro=libro,
            ))

        pedido.detalles = detalles
        db.commit()
        db.refresh(pedido)
        items = [
            {
                "libro_id": detalle.libro_id,
                "titulo": detalle.libro.titulo,
                "cantidad": detalle.cantidad,
                "precio_unitario": detalle.precio_unitario,
                "subtotal": detalle.cantidad * detalle.precio_unitario,
            }
            for detalle in pedido.detalles
        ]
        return {
            "pedido_id": pedido.pedido_id,
            "cliente_id": pedido.cliente_id,
            "estado": pedido.estado,
            "fecha_pedido": pedido.fecha_pedido,
            "total": sum((item["subtotal"] for item in items), Decimal("0")),
            "items": items,
        }
    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="No se pudo crear el pedido")


@app.get("/api/v1/pedidos/{pedido_id}", response_model=PedidoOut, tags=["Pedidos"])
def obtener_pedido(pedido_id: int, db: DbSession):
    pedido = db.scalar(
        select(Pedido).options(joinedload(Pedido.detalles).joinedload(DetallePedido.libro)).where(Pedido.pedido_id == pedido_id)
    )
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    items = [
        {
            "libro_id": detalle.libro_id,
            "titulo": detalle.libro.titulo,
            "cantidad": detalle.cantidad,
            "precio_unitario": detalle.precio_unitario,
            "subtotal": detalle.cantidad * detalle.precio_unitario,
        }
        for detalle in pedido.detalles
    ]
    return {
        "pedido_id": pedido.pedido_id,
        "cliente_id": pedido.cliente_id,
        "estado": pedido.estado,
        "fecha_pedido": pedido.fecha_pedido,
        "total": sum((item["subtotal"] for item in items), Decimal("0")),
        "items": items,
    }


@app.get("/api/v1/reportes/resumen", tags=["Reportes"])
def resumen(db: DbSession):
    clientes = db.scalar(select(func.count()).select_from(Cliente))
    libros = db.scalar(select(func.count()).select_from(Libro))
    pedidos = db.scalar(select(func.count()).select_from(Pedido))
    ventas = db.scalar(select(func.coalesce(func.sum(DetallePedido.cantidad * DetallePedido.precio_unitario), 0)))
    return {"clientes": clientes, "libros": libros, "pedidos": pedidos, "ventas": ventas}
