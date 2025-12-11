import os
from psycopg import connect
from psycopg.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return connect(
        host=os.getenv("PG_HOST"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASS"),
        dbname=os.getenv("PG_DB"),
        port=os.getenv("PG_PORT"),
        cursor_factory=RealDictCursor
    )


def insert_signal(event_ts, source, tag, velocity, delta, csi, category):
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
                (event_ts, source, tag, velocity, delta, csi, category)
            )
