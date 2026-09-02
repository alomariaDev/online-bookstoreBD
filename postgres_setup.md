# PostgreSQL local

La configuración de `docker-compose.yml` crea el servidor PostgreSQL, carga `schema_libreria.sql` y migra los CSV al inicializar la base por primera vez.

## Inicio

1. Instala Docker Desktop o Docker Engine con el complemento Compose.
2. Copia la configuración y asigna una contraseña propia:

   ```bash
   cp .env.example .env
   ```

3. Inicia PostgreSQL con el esquema y los datos:

   ```bash
   docker compose up -d
   ```

   La migración carga 500 clientes, 500 libros, 500 pedidos y 500 líneas de detalle.

4. Conéctate desde la terminal:

   ```bash
   docker compose exec postgres psql -U bookstore_user -d online_bookstorebd
   ```

El servidor queda disponible en `localhost:5432`. En pgAdmin usa los valores de `.env` para host, puerto, usuario, contraseña y base de datos.

## Reiniciar la base desde cero

Los scripts de inicialización solo se ejecutan al crear el volumen por primera vez. Para borrar los datos locales y volver a ejecutar el esquema y la migración:

```bash
docker compose down -v
docker compose up -d
```
