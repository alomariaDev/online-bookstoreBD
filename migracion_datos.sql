-- Migracion de Books.csv, Customers.csv y Orders.csv al modelo normalizado.
-- Ejecutar con psql desde este directorio:
-- psql -U bookstore_user -d online_bookstorebd -f migracion_datos.sql

BEGIN;

CREATE TEMP TABLE staging_books (
    book_id BIGINT,
    title TEXT,
    author TEXT,
    genre TEXT,
    published_year SMALLINT,
    price NUMERIC(10, 2),
    stock INTEGER
);

CREATE TEMP TABLE staging_customers (
    customer_id BIGINT,
    name TEXT,
    email TEXT,
    phone TEXT,
    city TEXT,
    country TEXT
);

CREATE TEMP TABLE staging_orders (
    order_id BIGINT,
    customer_id BIGINT,
    book_id BIGINT,
    order_date TEXT,
    quantity INTEGER,
    total_amount NUMERIC(10, 2)
);

\copy staging_books FROM '/data/Books.csv' WITH (FORMAT csv, HEADER true)
\copy staging_customers FROM '/data/Customers.csv' WITH (FORMAT csv, HEADER true)
\copy staging_orders FROM '/data/Orders.csv' WITH (FORMAT csv, HEADER true)

TRUNCATE TABLE detalle_pedido, pedidos, libros, clientes RESTART IDENTITY CASCADE;

INSERT INTO clientes (
    cliente_id, nombre, email, telefono, ciudad, pais
)
SELECT customer_id, name, email, phone, city, country
FROM staging_customers
ORDER BY customer_id;

INSERT INTO libros (
    libro_id, titulo, autor, genero, anio_publicacion, precio, stock
)
SELECT book_id, title, author, genre, published_year, price, stock
FROM staging_books
ORDER BY book_id;

INSERT INTO pedidos (
    pedido_id, cliente_id, fecha_pedido
)
SELECT order_id,
       customer_id,
       to_date(order_date, 'DD-MM-YYYY')::timestamptz
FROM staging_orders
ORDER BY order_id;

INSERT INTO detalle_pedido (
    detalle_id, pedido_id, libro_id, cantidad, precio_unitario
)
SELECT order_id,
       order_id,
       book_id,
       quantity,
       price
FROM staging_orders
JOIN staging_books USING (book_id)
ORDER BY order_id;

SELECT setval(
    pg_get_serial_sequence('clientes', 'cliente_id'),
    COALESCE(MAX(cliente_id), 1),
    MAX(cliente_id) IS NOT NULL
)
FROM clientes;

SELECT setval(
    pg_get_serial_sequence('libros', 'libro_id'),
    COALESCE(MAX(libro_id), 1),
    MAX(libro_id) IS NOT NULL
)
FROM libros;

SELECT setval(
    pg_get_serial_sequence('pedidos', 'pedido_id'),
    COALESCE(MAX(pedido_id), 1),
    MAX(pedido_id) IS NOT NULL
)
FROM pedidos;

SELECT setval(
    pg_get_serial_sequence('detalle_pedido', 'detalle_id'),
    COALESCE(MAX(detalle_id), 1),
    MAX(detalle_id) IS NOT NULL
)
FROM detalle_pedido;

COMMIT;

-- Comprobacion rapida de filas migradas.
SELECT 'clientes' AS tabla, COUNT(*) AS filas FROM clientes
UNION ALL
SELECT 'libros', COUNT(*) FROM libros
UNION ALL
SELECT 'pedidos', COUNT(*) FROM pedidos
UNION ALL
SELECT 'detalle_pedido', COUNT(*) FROM detalle_pedido;