import requests
from datetime import datetime
from pipeline.utils.db import insert_signal

HEADERS = {"User-Agent": "signal-engine/1.0"}

SUBREDDITS = [
    # Core mechanics & genres
    "roguelikes",
    "roguelikedev",
    "deckbuilding",
    "strategy",
    "strategygames",
    "simulationgames",

    # Dev-focused (early signals)
    "gamedev",
    "indiegames",
    "indiedev",
    "gameideas",

    # Systems & depth
    "4Xgaming",
    "basebuilding",
    "automationgames",
    "colonygames",

    # Emerging formats
    "survivorslikes",
    "autobattler",
    "tacticalgames",
    "proceduralgeneration"
]

KEYWORDS = [
    # Deck / card mechanics
    "deckbuilder",
    "deck-building",
    "card synergy",

    # Roguelike / procedural
    "roguelike",
    "procedural",
    "permadeath",

    # Automation / systems
    "automation",
    "factory",
    "resource loop",

    # Tactical / strategy
    "tactical",
    "turn-based",
    "grid-based",

    # Survivor-like / extraction
    "survivor-like",
    "bullet heaven",
    "extraction",

    # Meta / design signals
    "replayability",
    "emergent gameplay",
    "systems-driven"
]

POST_LIMIT = 50


def fetch_posts(subreddit):
    url = f"https://www.reddit.com/r/{subreddit}/new.json?limit={POST_LIMIT}"
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    return resp.json().get("data", {}).get("children", [])


def run():
    for subreddit in SUBREDDITS:
        try:
            posts = fetch_posts(subreddit)
        except Exception:
            continue

        for kw in KEYWORDS:
            matches = []

            for p in posts:
                data = p.get("data", {})
                text = (
                    (data.get("title") or "") + " " +
                    (data.get("selftext") or "")
                ).lower()

                if kw in text:
                    matches.append(data)

            if not matches:
                continue

            upvotes = [m.get("ups", 0) for m in matches]
            comments = [m.get("num_comments", 0) for m in matches]

            # --- Deterministic math ---
            velocity = min((sum(upvotes) + sum(comments)) / 600, 1)
            delta = min(len(matches) / 12, 1)
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
