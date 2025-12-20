import os
import psycopg
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def execute_view(view_path):
    """Execute a SQL view file against the database"""
    conn = None
    cursor = None
    try:
        # Database connection parameters
        db_params = {
            'host': os.getenv('PG_HOST', 'localhost'),
            'port': os.getenv('PG_PORT', '5432'),
            'dbname': os.getenv('PG_DB', 'signals_db'),
            'user': os.getenv('PG_USER', 'postgres'),
            'password': os.getenv('PG_PASS', 'bisquit')
        }
        
        # Read the SQL file
        with open(view_path, 'r') as file:
            sql_content = file.read()
        
        # Connect to database and execute
        conn = psycopg.connect(**db_params)
        cursor = conn.cursor()
        
        cursor.execute(sql_content)
        conn.commit()
        
        print(f"View executed successfully: {os.path.basename(view_path)}")
        
    except Exception as e:
        print(f"Error executing view {view_path}: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def run_views():
    """Execute all SQL view files in the views directory"""
    views_dir = "/home/mod/github/dri/views/views"
    
    if not os.path.exists(views_dir):
        print(f"Views directory not found: {views_dir}")
        return
    
    # Find all SQL files in the views directory
    sql_files = [f for f in os.listdir(views_dir) if f.endswith('.sql')]
    
    if not sql_files:
        print("No SQL view files found")
        return
    
    print(f"Executing {len(sql_files)} view(s)...")
    
    for sql_file in sql_files:
        view_path = os.path.join(views_dir, sql_file)
        execute_view(view_path)
    
    print("All views executed successfully.")

if __name__ == "__main__":
    run_views()
