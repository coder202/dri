import os
from dotenv import load_dotenv
load_dotenv()

try:
    import psycopg
except ImportError as e:
    raise ImportError(
        "psycopg (v3) is required to use the PostgreSQL backend.\n"
        "Install it with: pip install 'psycopg[binary]'"
    ) from e


def get_connection():
    """Return a new psycopg connection using environment variables.

    Expected environment variables (examples):
      - PG_HOST (default: 'localhost')
      - PG_USER (default: 'postgres')
      - PG_PASS (default: '')
      - PG_DB   (default: 'postgres')
      - PG_PORT (default: 5432)
    """
    host = os.getenv("PG_HOST", "localhost")
    user = os.getenv("PG_USER", "postgres")
    password = os.getenv("PG_PASS", "")
    dbname = os.getenv("PG_DB", "postgres")
    port = int(os.getenv("PG_PORT", 5432))

    return psycopg.connect(
        host=host,
        user=user,
        password=password,
        dbname=dbname,
        port=port,
    )


def insert_signal(event_ts, source, tag, velocity, delta, csi, category):
    """Insert a signal row into the `signals` table.

    This function assumes a real PostgreSQL instance is reachable. It will
    raise errors from the DB driver on failure so issues are visible.
    """
    sql = """
        INSERT INTO signals (
            event_ts, signal_source, tag, velocity, delta, CSI, category
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                sql,
                (event_ts, source, tag, velocity, delta, csi, category),
            )
        conn.commit()
