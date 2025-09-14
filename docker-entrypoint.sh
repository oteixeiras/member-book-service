#!/usr/bin/env sh
set -e

echo "[entrypoint] Waiting for database..."
# simple wait loop if needed; users can override in their orchestrator
sleep 2

if [ -f "alembic.ini" ]; then
  echo "[entrypoint] Running migrations..."
  alembic upgrade head || {
    echo "[entrypoint] Migrations failed" >&2
    exit 1
  }
fi

echo "[entrypoint] Starting server..."
exec gunicorn app.main:app \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --workers ${WORKERS:-2} \
  --log-level ${LOG_LEVEL:-info} \
  --timeout ${TIMEOUT:-60}


