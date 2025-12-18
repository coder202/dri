import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from sources.steam_tags import run as steam_run
from sources.google_trends import run as google_run
from sources.ai_signal_model import run as ai_run
from sources.reddit_velocity import run as reddit_run
from sources.github_activity import run as github_run

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

    try:
        reddit_run()
        print("Reddit velocity ingested.")
    except Exception as e:
        print("Reddit ingestion error:", e)
        
    try:
        github_run()
        print("GitHub activity ingested.")
    except Exception as e:
        print("GitHub ingestion error:", e)

    print("Pipeline complete.")
