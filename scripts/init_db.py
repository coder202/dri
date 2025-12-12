"""Run SQL migrations against configured Postgres instance.

Usage:
  python3 scripts/init_db.py

This reads environment variables (optionally from a `.env` file) and executes
`pipeline/migrations/create_signals.sql`.
"""
import os
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
except Exception:
    def load_dotenv():
        return

load_dotenv()

SQL_PATH = Path(__file__).resolve().parents[1] / "pipeline" / "migrations" / "create_signals.sql"

PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = int(os.getenv("PG_PORT", 5432))
PG_USER = os.getenv("PG_USER", "postgres")
PG_PASS = os.getenv("PG_PASS", "")
PG_DB = os.getenv("PG_DB", "postgres")


def run_sql_file(sql_file_path: Path):
    if not sql_file_path.exists():
        print(f"SQL file not found: {sql_file_path}")
        sys.exit(1)

    with open(sql_file_path, "r", encoding="utf-8") as f:
        sql = f.read()

    try:
        import psycopg
    except ImportError:
        print("psycopg (v3) is required to run migrations. Install with: pip install 'psycopg[binary]'")
        sys.exit(1)

    # Build connection kwargs, omitting password if empty (for trust auth)
    conn_kwargs = {
        "host": PG_HOST,
        "port": PG_PORT,
        "user": PG_USER,
        "dbname": PG_DB,
    }
    if PG_PASS:
        conn_kwargs["password"] = PG_PASS

    with psycopg.connect(**conn_kwargs) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()
        print("Migration applied successfully")


if __name__ == "__main__":
    run_sql_file(SQL_PATH)
