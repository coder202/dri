import requests
from datetime import datetime
from utils.db import insert_signal

STEAMSPY_API = "https://steamspy.com/api.php"

# Emerging / asymmetric categories
EMERGING_TAGS = {
    "Auto Battler": "auto-battler",
    "Deckbuilder": "deckbuilder",
    "Automation": "automation",
    "Colony Sim": "colony-sim",
    "Survivor-like": "survivor-like",
    "Extraction": "extraction",
    "Tactical Roguelike": "tactical-roguelike"
}

def fetch_top_indies():
    params = {
        "request": "top100in2weeks"
    }
    resp = requests.get(STEAMSPY_API, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json().values()


def run():
    games = fetch_top_indies()

    for label, tag in EMERGING_TAGS.items():
        matching = []

        for g in games:
            genres = (g.get("genre") or "").lower()
            tags = (g.get("tags") or "").lower()

            if tag.replace("-", " ") in genres or tag.replace("-", " ") in tags:
                matching.append(g)

        if not matching:
            continue

        owners = [g.get("owners", 0) for g in matching]
        reviews = [
            (g.get("positive", 0) + g.get("negative", 0))
            for g in matching
        ]

        avg_owners = sum(owners) / len(owners)
        avg_reviews = sum(reviews) / len(reviews)

        # --- Signal math (asymmetric by design) ---
        velocity = min(avg_reviews / 2_000, 1)           # attention acceleration
        delta = max(0, 1 - (avg_owners / 500_000))        # early-stage penalty
        csi = min((velocity * 0.7 + delta * 0.3), 1)

        insert_signal(
            event_ts=datetime.utcnow(),
            source="steam_spy",
            tag=tag,
            velocity=round(velocity, 6),
            delta=round(delta, 6),
            csi=round(csi, 6),
            category="emerging-category"
        )
