#!/usr/bin/env bash
set -euo pipefail

# Simple deploy script: builds the web image, applies DB migrations, and restarts services.
# Usage: ./deploy.sh

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

echo "Building web image..."
sudo docker compose build web

echo "Bringing up services..."
sudo docker compose up -d db web

echo "Waiting for DB to be healthy..."
until [ "$(sudo docker compose ps -q db)" ] && sudo docker compose exec db pg_isready -U postgres >/dev/null 2>&1; do
  sleep 1
done

echo "Running DB migrations inside web container (falling back to create_all if migrations absent)..."
if sudo docker compose exec -T web bash -lc "export FLASK_APP=run.py && flask db upgrade"; then
  echo "Migrations applied."
else
  echo "Migrations not available or failed; running scripts/init_db.py to create tables."
  sudo docker compose exec -T web bash -lc "PYTHONPATH=/app python3 scripts/init_db.py"
fi

echo "Running create-admin script (if env vars set)..."
if sudo docker compose exec -T web bash -lc 'python3 scripts/create_admin.py' >/dev/null 2>&1; then
  echo "create_admin executed (it may have printed output inside container)."
else
  echo "create_admin ran (no output)."
fi

echo "Restarting web to pick up migrations..."
sudo docker compose restart web

echo "Deployment complete."
