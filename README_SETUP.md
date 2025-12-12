# DRI Pipeline

A data ingestion pipeline that collects signals from Steam, Google Trends, and an AI model, storing them in PostgreSQL.

## Quick Start

### Option 1: Run locally with Docker networking (recommended)

```bash
# 1. Start Postgres
docker compose -f docker.yaml up -d

# 2. Wait for Postgres to initialize
sleep 5

# 3. Run pipeline in Docker (avoids host TCP auth issues)
docker run --rm \
  --network dri_default \
  -v "$PWD":/app \
  -w /app \
  -e PG_HOST=postgres_container \
  -e PG_USER=driuser \
  -e PG_PASS=dripass \
  -e PG_DB=dridb \
  python:3.12 \
  bash -c "pip install -q -r requirements.txt && python3 pipeline/main.py"
```

### Option 2: Setup for local development (venv)

```bash
# 1. Start Postgres
docker compose -f docker.yaml up -d

# 2. Copy and edit environment file
cp .env.example .env
# Edit .env with proper credentials if needed

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run pipeline (Note: this will fail to connect from WSL host to Postgres on localhost)
python3 pipeline/main.py
```

**Note**: On WSL/Windows, Postgres port forwarding may not work properly from the host. Use Option 1 (Docker) for reliable execution.

## Project Structure

```
pipeline/
  main.py              # Entry point
  sources/             # Data sources
    steam_tags.py      # Steam gaming data
    google_trends.py   # Google Trends data
    ai_signal_model.py # AI-generated signals
  utils/
    db.py              # PostgreSQL connection and insert logic
  migrations/
    create_signals.sql # Database schema
scripts/
  init_db.py           # Migration runner
docker.yaml            # Postgres container definition
requirements.txt       # Python dependencies
```

## Configuration

Environment variables (from `.env`):
- `PG_HOST` — Postgres server hostname (default: `localhost`)
- `PG_PORT` — Postgres port (default: `5432`)
- `PG_USER` — Postgres username (default: `postgres`)
- `PG_PASS` — Postgres password (default: empty)
- `PG_DB` — Database name (default: `postgres`)

## Database

The pipeline stores all ingested signals in a `signals` table with the following schema:

```sql
CREATE TABLE signals (
  id SERIAL PRIMARY KEY,
  event_ts TIMESTAMP NOT NULL,
  signal_source TEXT,     -- 'steam_spy', 'google_trends', 'ai_model'
  tag TEXT,               -- game genre, search term, etc.
  velocity REAL,
  delta REAL,
  CSI REAL,               -- Combined Signal Index
  category TEXT,          -- 'gaming', 'consumer', 'future-signals'
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

## Dependencies

- **psycopg[binary]** — PostgreSQL driver (v3)
- **requests** — HTTP client for data fetching
- **python-dotenv** — Environment variable loader

## Troubleshooting

### Pipeline runs but DB inserts fail
- **Cause**: Postgres not running or unreachable
- **Fix**: Start Postgres with `docker compose -f docker.yaml up -d` or ensure it's running on the configured host/port

### "connection to server failed: fe_sendauth: no password supplied"
- **Cause**: Running from WSL/Windows host with improper TCP forwarding
- **Fix**: Use Option 1 above (Docker) or run from within a Linux container

### "name 'json' is not defined"
- **Cause**: requests module import failed
- **Fix**: Ensure `requests` is installed (`pip install -r requirements.txt`)

## License

See LICENSE file
