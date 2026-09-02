-- Esquema normalizado para una librería en línea (PostgreSQL)
-- Un pedido puede contener uno o varios libros mediante detalle_pedido.

DROP TABLE IF EXISTS detalle_pedido;
DROP TABLE IF EXISTS pedidos;
DROP TABLE IF EXISTS libros;
DROP TABLE IF EXISTS clientes;

CREATE TABLE clientes (
    cliente_id BIGSERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    telefono VARCHAR(20),
    ciudad VARCHAR(80),
    pais VARCHAR(80),
    creado_en TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE libros (
    libro_id BIGSERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    autor VARCHAR(150) NOT NULL,
    genero VARCHAR(80),
    anio_publicacion SMALLINT CHECK (anio_publicacion BETWEEN 1000 AND 2100),
    isbn VARCHAR(17) UNIQUE,
    precio NUMERIC(10, 2) NOT NULL CHECK (precio >= 0),
    stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0)
);

CREATE TABLE pedidos (
    pedido_id BIGSERIAL PRIMARY KEY,
    cliente_id BIGINT NOT NULL REFERENCES clientes(cliente_id),
    fecha_pedido TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    estado VARCHAR(20) NOT NULL DEFAULT 'pendiente'
        CHECK (estado IN ('pendiente', 'pagado', 'enviado', 'cancelado'))
);

CREATE TABLE detalle_pedido (
    detalle_id BIGSERIAL PRIMARY KEY,
    pedido_id BIGINT NOT NULL REFERENCES pedidos(pedido_id) ON DELETE CASCADE,
    libro_id BIGINT NOT NULL REFERENCES libros(libro_id),
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario NUMERIC(10, 2) NOT NULL CHECK (precio_unitario >= 0),
    CONSTRAINT uq_detalle_pedido_libro UNIQUE (pedido_id, libro_id)
);

CREATE INDEX idx_pedidos_cliente_id ON pedidos(cliente_id);
CREATE INDEX idx_detalle_pedido_libro_id ON detalle_pedido(libro_id);

-- Total de un pedido:
-- SELECT p.pedido_id, SUM(dp.cantidad * dp.precio_unitario) AS total
-- FROM pedidos p
-- JOIN detalle_pedido dp ON dp.pedido_id = p.pedido_id
-- GROUP BY p.pedido_id;
