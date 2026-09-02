# Modelo entidad–relación: librería en línea

Este modelo normaliza la tabla `Orders` original: un pedido puede tener varios libros y cada línea conserva el precio que tenía el libro al momento de la compra.

```mermaid
erDiagram
    CLIENTES ||--o{ PEDIDOS : realiza
    PEDIDOS ||--|{ DETALLE_PEDIDO : contiene
    LIBROS ||--o{ DETALLE_PEDIDO : aparece_en

    CLIENTES {
        bigint cliente_id PK
        varchar nombre
        varchar email UK
        varchar telefono
        varchar ciudad
        varchar pais
        timestamptz creado_en
    }
    LIBROS {
        bigint libro_id PK
        varchar titulo
        varchar autor
        varchar genero
        smallint anio_publicacion
        varchar isbn UK
        numeric precio
        integer stock
    }
    PEDIDOS {
        bigint pedido_id PK
        bigint cliente_id FK
        timestamptz fecha_pedido
        varchar estado
    }
    DETALLE_PEDIDO {
        bigint detalle_id PK
        bigint pedido_id FK
        bigint libro_id FK
        integer cantidad
        numeric precio_unitario
    }
```

## Cardinalidades

- Un cliente puede realizar cero o muchos pedidos; cada pedido pertenece a un único cliente.
- Un pedido contiene una o más líneas de detalle.
- Un libro puede no haberse vendido o aparecer en muchas líneas de detalle.
- `detalle_pedido` resuelve la relación muchos-a-muchos entre pedidos y libros.
