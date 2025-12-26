import feedparser
from datetime import datetime
from utils.db import insert_signal

# Stack Overflow tag RSS feeds
TAGS = {
    "procedural-generation": "procedural-generation",
    "game-ai": "tactical-ai",
    "pathfinding": "tactical-ai",
    "reinforcement-learning": "rl-agents",
    "unity": "game-engines",
    "godot": "game-engines",
    "unreal-engine": "game-engines",
    "deck-building": "deckbuilder",
    "roguelike": "roguelike",
    "automation": "automation"
}

BASE_FEED = "https://stackoverflow.com/feeds/tag?tagnames={tag}&sort=newest"

POST_LIMIT = 30
BASELINE_DIVISOR = 15  # normalization constant


def fetch_tag_activity(tag):
    feed = feedparser.parse(BASE_FEED.format(tag=tag))
    return feed.entries[:POST_LIMIT]


def run():
    for so_tag, canonical_tag in TAGS.items():
        try:
            entries = fetch_tag_activity(so_tag)
        except Exception:
            continue

        if not entries:
            continue

        # Count activity
        posts = len(entries)
        recent = entries[:10]

        # Engagement proxy (questions + answers + comments inferred)
        activity_score = posts + sum(
            int(e.get("slash_comments", 0) or 0) for e in recent
        )

        # --- Deterministic normalization ---
        velocity = min(activity_score / 50, 1)
        delta = min(posts / BASELINE_DIVISOR, 1)
        csi = min((velocity * 0.6 + delta * 0.4), 1)

        insert_signal(
            event_ts=datetime.utcnow(),
            source="stackoverflow_trends",
            tag=canonical_tag,
            velocity=round(velocity, 6),
            delta=round(delta, 6),
            csi=round(csi, 6),
            category="developer-attention"
        )
