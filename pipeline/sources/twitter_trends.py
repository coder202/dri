import os
import requests
from datetime import datetime
from utils.db import insert_signal
from dotenv import load_dotenv

load_dotenv()

BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "User-Agent": "signal-ingestion-bot/1.0"
}

# WOEID 1 = Worldwide trends
TRENDS_URL = "https://api.twitter.com/1.1/trends/place.json?id=1"


def run():
    if not BEARER_TOKEN:
        raise RuntimeError("Missing TWITTER_BEARER_TOKEN in environment")

    resp = requests.get(TRENDS_URL, headers=HEADERS, timeout=10)
    resp.raise_for_status()

    trends = resp.json()[0].get("trends", [])

    for t in trends:
        tag = t.get("name")
        tweet_volume = t.get("tweet_volume") or 0

        # Normalize metrics
        velocity = min(tweet_volume / 100_000, 1)          # attention intensity
        delta = min(len(tag) / 50, 1) if tag else 0         # structural spread proxy
        csi = min((velocity * 0.75 + delta * 0.25), 1)      # composite signal index

        insert_signal(
            event_ts=datetime.utcnow(),
            source="twitter_trends",
            tag=tag,
            velocity=round(velocity, 6),
            delta=round(delta, 6),
            csi=round(csi, 6),
            category="social-attention"
        )
