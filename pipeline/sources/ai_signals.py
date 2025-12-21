import requests
import feedparser
from datetime import datetime
from pipeline.utils.db import insert_signal

HEADERS = {"User-Agent": "signal-engine/1.0"}

# AI capability → game / system impact mapping
KEYWORDS = {
    "reinforcement learning": "rl-agents",
    "procedural generation": "procedural-generation",
    "large language model": "llm-tools",
    "llm": "llm-tools",
    "diffusion": "content-generation",
    "generative ai": "content-generation",
    "autonomous agent": "ai-agents",
    "multi-agent": "ai-agents",
    "pathfinding ai": "tactical-ai",
    "decision tree": "tactical-ai"
}

# ---------------------------
# Hacker News
# ---------------------------

HN_TOP_STORIES = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM = "https://hacker-news.firebaseio.com/v0/item/{}.json"


def fetch_hn_mentions():
    try:
        ids = requests.get(HN_TOP_STORIES, timeout=10).json()[:100]
    except Exception:
        return {}

    counts = {k: 0 for k in KEYWORDS}

    for sid in ids:
        try:
            item = requests.get(HN_ITEM.format(sid), timeout=10).json()
        except Exception:
            continue

        text = ((item.get("title") or "") + " " +
                (item.get("text") or "")).lower()

        for kw in KEYWORDS:
            if kw in text:
                counts[kw] += 1

    return counts


# ---------------------------
# GitHub Trending (lightweight)
# ---------------------------

def fetch_github_trending():
    url = "https://github.com/trending?since=daily"
    try:
        html = requests.get(url, headers=HEADERS, timeout=10).text.lower()
    except Exception:
        return {}

    counts = {k: 0 for k in KEYWORDS}
    for kw in KEYWORDS:
        counts[kw] = html.count(kw)

    return counts


# ---------------------------
# arXiv AI RSS
# ---------------------------

def fetch_arxiv_mentions():
    feed = feedparser.parse("http://export.arxiv.org/rss/cs.AI")
    counts = {k: 0 for k in KEYWORDS}

    for entry in feed.entries[:50]:
        text = (entry.title + " " + entry.summary).lower()
        for kw in KEYWORDS:
            if kw in text:
                counts[kw] += 1

    return counts


# ---------------------------
# Signal synthesis
# ---------------------------

def run():
    hn = fetch_hn_mentions()
    gh = fetch_github_trending()
    arx = fetch_arxiv_mentions()

    for kw, tag in KEYWORDS.items():
        hn_c = hn.get(kw, 0)
        gh_c = gh.get(kw, 0)
        arx_c = arx.get(kw, 0)

        total = hn_c + gh_c + arx_c
        if total == 0:
            continue

        # --- Deterministic normalization ---
        velocity = min(total / 15, 1)
        delta = min((hn_c + gh_c) / 10, 1)
        csi = min((velocity * 0.5 + delta * 0.5), 1)

        insert_signal(
            event_ts=datetime.utcnow(),
            source="ai_signals",
            tag=tag,
            velocity=round(velocity, 6),
            delta=round(delta, 6),
            csi=round(csi, 6),
            category="capability-shift"
        )
