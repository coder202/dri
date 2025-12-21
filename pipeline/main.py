import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from sources.steam_spy import run as steam_spy_run
from sources.steam_tags import run as steam_run
from sources.ai_signals import run as ai_signals_run
from sources.reddit_velocity import run as reddit_run
from sources.reddit_trends import run as reddit_trends_run
from sources.github_activity import run as github_run
from sources.itchio_new_releases import run as itchio_run
from sources.steam_tag_growth import run as steam_tag_run
from sources.wikipedia_pageviews import run as wiki_run
from sources.steam_emerging import run as steam_emerging_run
from utils.views import run_views

if __name__ == "__main__":
    print("Starting ingestion pipeline...")
    
    try:
        steam_spy_run()
        print("Steam Spy data ingested.")
    except Exception as e:
        print("Steam Spy ingestion error:", e)

    try:
        steam_run()
        print("Steam data ingested.")
    except Exception as e:
        print("Steam ingestion error:", e)

    try:
        steam_emerging_run()
        print("Steam emerging categories ingested.")
    except Exception as e:
        print("Steam emerging ingestion error:", e)

    try:
        steam_tag_run()
        print("Steam tag growth ingested.")
    except Exception as e:
        print("Steam tag growth ingestion error:", e)

    try:
        ai_signals_run()
        print("AI signals ingested.")
    except Exception as e:
        print("AI signals ingestion error:", e)

    try:
        reddit_run()
        print("Reddit velocity ingested.")
    except Exception as e:
        print("Reddit ingestion error:", e)

    try:
        reddit_trends_run()
        print("Reddit trends ingested.")
    except Exception as e:
        print("Reddit trends ingestion error:", e)
        
    try:
        github_run()
        print("GitHub activity ingested.")
    except Exception as e:
        print("GitHub ingestion error:", e)

    try:
        itchio_run()
        print("itch.io new releases ingested.")
    except Exception as e:
        print("itch.io ingestion error:", e)

    try:
        wiki_run()
        print("Wikipedia pageviews ingested.")
    except Exception as e:
        print("Wikipedia pageviews ingestion error:", e)

    try:
        run_views()
        print("Database views updated.")
    except Exception as e:
        print("Views execution error:", e)

    print("Pipeline complete.")
