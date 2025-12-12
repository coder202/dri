import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from sources.steam_tags import run as steam_run
from sources.google_trends import run as google_run
from sources.ai_signal_model import run as ai_run

if __name__ == "__main__":
    print("Starting ingestion pipeline...")
    
    try:
        steam_run()
        print("Steam data ingested.")
    except Exception as e:
        print("Steam ingestion error:", e)

    try:
        google_run()
        print("Google Trends ingested.")
    except Exception as e:
        print("Google ingestion error:", e)

    try:
        ai_run()
        print("AI model ingested.")
    except Exception as e:
        print("AI ingestion error:", e)

    print("Pipeline complete.")
