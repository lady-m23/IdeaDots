#!/usr/bin/env bash
# Runs `flutter run` with the dart-defines from .env.<env>.
# Usage: tool/run_with_env.sh <dev|prod> [flutter run args...]
set -euo pipefail

cd "$(dirname "$0")/.."

env_name="${1:-}"
if [[ "$env_name" != "dev" && "$env_name" != "prod" ]]; then
  echo "Usage: $0 <dev|prod> [flutter run args...]" >&2
  exit 64
fi
shift

env_file=".env.${env_name}"
if [[ ! -f "$env_file" ]]; then
  echo "Missing $env_file. Copy .env.example to $env_file and fill in the Supabase values." >&2
  exit 1
fi

declared_env="$(grep -E '^ENV=' "$env_file" | tail -n 1 | cut -d= -f2- | tr -d '[:space:]"' || true)"
if [[ "$declared_env" != "$env_name" ]]; then
  echo "$env_file must contain ENV=$env_name (found '${declared_env}')." >&2
  exit 1
fi

exec flutter run --dart-define-from-file="$env_file" "$@"
