import requests
from datetime import datetime, timedelta
from pipeline.utils.db import insert_signal

HEADERS = {
    "User-Agent": "signal-engine/1.0 (contact: coder202@gmx.com)"
}

WIKI_API = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article"

PROJECT = "en.wikipedia"
ACCESS = "all-access"
AGENT = "user"

# Canonical pages mapped to mechanics / categories
PAGES = {
    "Deck-building_game": "deckbuilder",
    "Roguelike": "roguelike",
    "Procedural_generation": "procedural-generation",
    "Automation": "automation",
    "Turn-based_strategy": "tactical",
    "4X": "4x-strategy",
    "Base-building_game": "base-building",
    "Survivor-like": "survivor-like"
}

DAYS_LOOKBACK = 14
MIN_VIEWS_THRESHOLD = 500


def fetch_pageviews(article, start, end):
    url = f"{WIKI_API}/{PROJECT}/{ACCESS}/{AGENT}/{article}/daily/{start}/{end}"
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    items = resp.json().get("items", [])
    return [i["views"] for i in items]


def run():
    end_date = datetime.utcnow() - timedelta(days=1)
    start_date = end_date - timedelta(days=DAYS_LOOKBACK - 1)

    start = start_date.strftime("%Y%m%d")
    end = end_date.strftime("%Y%m%d")

    for article, tag in PAGES.items():
        try:
            views = fetch_pageviews(article, start, end)
        except Exception:
            continue

        if len(views) < 7:
            continue

        total_views = sum(views)
        if total_views < MIN_VIEWS_THRESHOLD:
            continue

        # Split into baseline vs recent
        baseline = views[:7]
        recent = views[-7:]

        baseline_avg = sum(baseline) / len(baseline)
        recent_avg = sum(recent) / len(recent)

        # --- Deterministic signal math ---
        velocity = min(recent_avg / 10000, 1)
        delta = min(
            (recent_avg - baseline_avg) / baseline_avg
            if baseline_avg > 0 else 0,
            1
        )
        csi = min((velocity * 0.7 + delta * 0.3), 1)

        insert_signal(
            event_ts=datetime.utcnow(),
            source="wikipedia_pageviews",
            tag=tag,
            velocity=round(max(velocity, 0), 6),
            delta=round(max(delta, 0), 6),
            csi=round(max(csi, 0), 6),
            category="knowledge-demand"
        )
