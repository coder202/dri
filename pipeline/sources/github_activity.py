import requests
from datetime import datetime
from utils.db import insert_signal

KEYWORDS = [
    "procedural-generation",
    "game-ai",
    "roguelike",
    "pathfinding",
    "simulation-engine"
]

def run():
    headers = {"Accept": "application/vnd.github+json"}
    for kw in KEYWORDS:
        url = f"https://api.github.com/search/repositories?q={kw}&sort=updated"
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()

        repos = data.get("items", [])
        if not repos:
            continue

        recent_updates = [
            r for r in repos
            if r.get("pushed_at")
        ]

        velocity = len(recent_updates) / 10
        delta = sum(r.get("stargazers_count", 0) for r in recent_updates[:5]) / 1000
        csi = min((velocity * 0.5 + delta * 0.5), 1)

        insert_signal(
            event_ts=datetime.utcnow(),
            source="github_activity",
            tag=kw,
            velocity=round(velocity, 6),
            delta=round(delta, 6),
            csi=round(csi, 6),
            category="developer-supply"
        )
