#!/bin/sh
set -e

echo "⏳ Aguardando banco de dados..."

while ! nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 1
done

echo "✅ Banco disponível"

echo "🚀 Aplicando migrations..."
alembic upgrade head

echo "🎉 Migrations aplicadas"

# Executa o comando passado (uvicorn, futuramente celery, etc)
exec "$@"
