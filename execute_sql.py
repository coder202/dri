#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'pipeline'))

from utils.db import get_connection

def execute_sql_file(file_path):
    """Execute SQL from a file using the database connection."""
    with open(file_path, 'r') as f:
        sql_content = f.read()
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql_content)
        conn.commit()
    
    print(f"Successfully executed SQL from {file_path}")

if __name__ == "__main__":
    sql_file = "views/market_divergence_view_v2.sql"
    execute_sql_file(sql_file)
