#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
export PATH="$HOME/.fly/bin:$PATH"

echo "Ensuring flyctl is installed..."
if ! command -v flyctl >/dev/null 2>&1; then
  curl -L https://fly.io/install.sh | sh
  export PATH="$HOME/.fly/bin:$PATH"
fi

if [ -n "${FLY_API_TOKEN:-}" ]; then
  echo "Logging into Fly using FLY_API_TOKEN..."
  flyctl auth login --access-token "$FLY_API_TOKEN"
else
  echo "No FLY_API_TOKEN set — performing interactive login. Follow browser instructions."
  flyctl auth login
fi

echo "Deploying application using fly.toml (app: farmer-pocket)..."
flyctl deploy --config "$ROOT_DIR/fly.toml" --app=farmer-pocket

echo "Deploy finished."
