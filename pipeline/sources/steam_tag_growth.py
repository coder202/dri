import requests
from datetime import datetime
from utils.db import insert_signal

STEAMSPY_TAGS_URL = "https://steamspy.com/api.php?request=tagstats"

MIN_GAMES_THRESHOLD = 50


def fetch_tag_stats():
    resp = requests.get(STEAMSPY_TAGS_URL, timeout=15)
    resp.raise_for_status()
    return resp.json()


def run():
    try:
        tag_data = fetch_tag_stats()
    except Exception:
        return

    for raw_tag, stats in tag_data.items():
        try:
            total_games = int(stats.get("games", 0))
            delta_24h = int(stats.get("delta", 0))
        except Exception:
            continue

        if total_games < MIN_GAMES_THRESHOLD:
            continue

        # --- Deterministic growth math ---
        velocity = min(delta_24h / 100, 1)
        delta = min(delta_24h / max(total_games, 1), 1)
        csi = min((velocity * 0.6 + delta * 0.4), 1)

        insert_signal(
            event_ts=datetime.utcnow(),
            source="steam_tag_growth",
            tag=raw_tag.lower(),
            velocity=round(max(velocity, 0), 6),
            delta=round(max(delta, 0), 6),
            csi=round(max(csi, 0), 6),
            category="supply-pressure"
        )
