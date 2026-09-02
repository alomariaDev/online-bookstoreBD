# Online Bookstore API

Backend FastAPI conectado a PostgreSQL.

## Ejecutar con Docker

Desde la raiz del repositorio:

```bash
docker compose up -d --build
```

API: http://localhost:8000
Documentacion interactiva: http://localhost:8000/docs

## Ejecutar directamente en local

```bash
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env
.venv/bin/uvicorn app.main:app --reload --port 8000
```

## Endpoints principales

- `GET /health`
- `GET /api/v1/libros`
- `GET /api/v1/libros/{id}`
- `GET /api/v1/clientes/{id}`
- `POST /api/v1/pedidos`
- `GET /api/v1/pedidos/{id}`
- `GET /api/v1/reportes/resumen`
