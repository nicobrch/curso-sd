# Tarea 2

Correr contenedor docker con PostgreSQL
```bash
docker run --name postgres-t2sd -e POSTGRES_DB=t2sd -e POSTGRES_USER=root -e POSTGRES_PASSWORD=1234 -p 5432:5432 -d postgres:latest
```