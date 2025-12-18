import requests
from datetime import datetime, timedelta
from pipeline.utils.db import insert_signal

WIKI_API = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article"

PAGES = {
    "Procedural_generation": "procedural-generation",
    "Roguelike": "roguelike",
    "Game_AI": "game-ai",
    "Simulation_video_game": "simulation"
}

def run():
    end = datetime.utcnow() - timedelta(days=1)
    start = end - timedelta(days=7)

    start_str = start.strftime("%Y%m%d")
    end_str = end.strftime("%Y%m%d")
    
    headers = {
        'User-Agent': 'DRI-Pipeline/1.0 (https://github.com/mod/dri; contact@example.com)'
    }

    for page, tag in PAGES.items():
        try:
            url = f"{WIKI_API}/en.wikipedia/all-access/user/{page}/daily/{start_str}/{end_str}"
            resp = requests.get(url, timeout=10, headers=headers)
            
            # Check if request was successful
            if resp.status_code != 200:
                print(f"Wikipedia API error for {page}: HTTP {resp.status_code}")
                continue
                
            # Check if response is empty
            if not resp.text.strip():
                print(f"Wikipedia API returned empty response for {page}")
                continue
                
            data = resp.json()

            views = [d["views"] for d in data.get("items", [])]
            if not views:
                print(f"No view data found for {page}")
                continue

            avg_views = sum(views) / len(views)
            velocity = min(avg_views / 50_000, 1)
            delta = min((max(views) - min(views)) / avg_views, 1)
            csi = min((velocity * 0.5 + delta * 0.5), 1)

            insert_signal(
                event_ts=datetime.utcnow(),
                source="wikipedia_pageviews",
                tag=tag,
                velocity=round(velocity, 6),
                delta=round(delta, 6),
                csi=round(csi, 6),
                category="knowledge-interest"
            )
            
            print(f"Wikipedia data processed for {page}: {len(views)} days, avg views: {avg_views:.0f}")
            
        except requests.exceptions.RequestException as e:
            print(f"Request error for {page}: {e}")
            continue
        except ValueError as e:
            print(f"JSON parsing error for {page}: {e}")
            print(f"Response content: {resp.text[:200]}...")
            continue
        except Exception as e:
            print(f"Unexpected error for {page}: {e}")
            continue
