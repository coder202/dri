import feedparser
from datetime import datetime
from utils.db import insert_signal

ITCH_RSS = "https://itch.io/games/newest.xml"

KEYWORDS = [
    "strategy",
    "simulation",
    "tactical",
    "roguelike",
    "automation"
]

def run():
    feed = feedparser.parse(ITCH_RSS)
    entries = feed.entries[:50]

    for kw in KEYWORDS:
        matches = [
            e for e in entries
            if kw in (e.title + " " + e.get("summary", "")).lower()
        ]

        velocity = len(matches) / 10
        delta = velocity / 5
        csi = min((velocity * 0.7 + delta * 0.3), 1)

        insert_signal(
            event_ts=datetime.utcnow(),
            source="itchio_new_releases",
            tag=kw,
            velocity=round(velocity, 6),
            delta=round(delta, 6),
            csi=round(csi, 6),
            category="indie-innovation"
        )
