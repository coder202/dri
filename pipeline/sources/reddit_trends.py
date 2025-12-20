import requests
from datetime import datetime
from utils.db import insert_signal

SUBREDDITS = [
    "roguelikes",
    "deckbuilding",
    "gamedev",
    "indiegames",
    "strategy"
]

KEYWORDS = [
    "deckbuilder",
    "roguelike",
    "auto battler",
    "survivors",
    "automation"
]

def run():
    headers = {"User-Agent": "signal-engine/1.0"}

    for sub in SUBREDDITS:
        url = f"https://www.reddit.com/r/{sub}/new.json?limit=50"
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()

        posts = data.get("data", {}).get("children", [])

        for kw in KEYWORDS:
            matches = [
                p for p in posts
                if kw in (
                    p["data"]["title"] + " " +
                    p["data"].get("selftext", "")
                ).lower()
            ]

            if not matches:
                continue

            upvotes = [p["data"]["ups"] for p in matches]
            comments = [p["data"]["num_comments"] for p in matches]

            velocity = min((sum(upvotes) + sum(comments)) / 500, 1)
            delta = min(len(matches) / 10, 1)
            csi = min((velocity * 0.6 + delta * 0.4), 1)

            insert_signal(
                event_ts=datetime.utcnow(),
                source="reddit_trends",
                tag=kw,
                velocity=round(velocity, 6),
                delta=round(delta, 6),
                csi=round(csi, 6),
                category="social-attention"
            )
