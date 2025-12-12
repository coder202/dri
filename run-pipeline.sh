#!/bin/bash
# Run the DRI pipeline with PostgreSQL in Docker

set -e

DOCKER_IMAGE="${DOCKER_IMAGE:-python:3.12}"
NETWORK="${NETWORK:-dri_default}"
PG_HOST="${PG_HOST:-postgres_container}"
PG_USER="${PG_USER:-driuser}"
PG_PASS="${PG_PASS:-dripass}"
PG_DB="${PG_DB:-dridb}"

echo "Starting Postgres container..."
docker compose -f docker.yaml up -d

echo "Waiting for Postgres to be ready..."
sleep 5

echo "Running pipeline in Docker..."
docker run --rm \
  --network "$NETWORK" \
  -v "$(pwd)":/app \
  -w /app \
  -e PG_HOST="$PG_HOST" \
  -e PG_USER="$PG_USER" \
  -e PG_PASS="$PG_PASS" \
  -e PG_DB="$PG_DB" \
  "$DOCKER_IMAGE" \
  bash -c "pip install -q -r requirements.txt && python3 pipeline/main.py"

echo "Pipeline execution complete."
