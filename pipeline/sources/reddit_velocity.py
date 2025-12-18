import requests
from datetime import datetime
from utils.db import insert_signal

SUBREDDITS = [
    "gamedev",
    "indiegames",
    "roguelikes",
    "boardgames",
    "strategy"
]

def run():
    headers = {"User-Agent": "signal-bot/1.0"}
    for sub in SUBREDDITS:
        url = f"https://www.reddit.com/r/{sub}/new.json?limit=50"
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()

        posts = data.get("data", {}).get("children", [])
        if not posts:
            continue

        timestamps = [p["data"]["created_utc"] for p in posts]
        velocity = len(posts) / max((max(timestamps) - min(timestamps)) / 3600, 1)

        delta = velocity / 100
        csi = min((velocity * 0.6 + delta * 0.4), 1)

        insert_signal(
            event_ts=datetime.utcnow(),
            source="reddit_velocity",
            tag=sub,
            velocity=round(velocity, 6),
            delta=round(delta, 6),
            csi=round(csi, 6),
            category="community-demand"
        )
