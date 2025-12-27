#!/bin/bash
# Setup and run the DRI pipeline with PostgreSQL

set -e

echo "Starting Postgres container..."
docker compose -f docker.yaml down -v || true
docker compose -f docker.yaml up -d

echo "Waiting for Postgres to initialize..."
sleep 10

echo "Activating virtual environment..."
source ./venv/bin/activate

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Waiting for Postgres to be fully ready..."
sleep 5

echo "Running pipeline..."
export PG_HOST=localhost
export PG_USER=postgres
export PG_PASS=biscuit
export PG_DB=signals_db
export PG_PORT=5432
export PYTHONPATH=/home/mod/github/dri

python3 pipeline/main.py

echo "Pipeline complete!"
