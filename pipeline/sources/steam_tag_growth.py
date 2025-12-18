import requests
from datetime import datetime
from utils.db import insert_signal

STEAM_SEARCH_URL = "https://store.steampowered.com/api/storesearch/"

TAGS = [
    "Strategy",
    "Simulation",
    "Roguelike",
    "Deckbuilder",
    "Automation"
]

def run():
    for tag in TAGS:
        params = {
            "term": tag,
            "l": "english",
            "cc": "US"
        }

        resp = requests.get(STEAM_SEARCH_URL, params=params, timeout=10)
        data = resp.json()

        total = data.get("total", 0)
        items = data.get("items", [])

        velocity = min(total / 10_000, 1)
        delta = min(len(items) / 50, 1)
        csi = min((velocity * 0.6 + delta * 0.4), 1)

        insert_signal(
            event_ts=datetime.utcnow(),
            source="steam_tag_growth",
            tag=tag.lower(),
            velocity=round(velocity, 6),
            delta=round(delta, 6),
            csi=round(csi, 6),
            category="store-demand"
        )
