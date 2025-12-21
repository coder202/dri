#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'pipeline'))

from utils.db import get_connection

def drop_and_create_view():
    """Drop existing view and create new one."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            # Drop the existing view if it exists
            cur.execute("DROP VIEW IF EXISTS market_divergence_view")
            conn.commit()
            print("Existing view dropped")
    
    # Now execute the new view creation
    with open('views/market_divergence_snapshot_v2.sql', 'r') as f:
        sql_content = f.read()
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql_content)
        conn.commit()
    
    print("New view created successfully")

if __name__ == "__main__":
    drop_and_create_view()
