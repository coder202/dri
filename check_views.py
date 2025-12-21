#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'pipeline'))

from utils.db import get_connection

def check_views():
    """Check what views exist in the database."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            # Check if our specific view exists
            cur.execute("""
                SELECT table_name 
                FROM information_schema.views 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)
            views = cur.fetchall()
            
            print("Views in database:")
            for view in views:
                print(f"  - {view[0]}")
            
            # Try to query our view specifically
            try:
                cur.execute("SELECT COUNT(*) FROM market_divergence_view LIMIT 1")
                count = cur.fetchone()[0]
                print(f"\nmarket_divergence_view exists and has {count} rows")
            except Exception as e:
                print(f"\nmarket_divergence_view does not exist or error: {e}")

if __name__ == "__main__":
    check_views()
