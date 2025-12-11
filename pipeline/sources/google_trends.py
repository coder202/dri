import requests
from datetime import datetime
from utils.db import insert_signal

def run():
    url = "https://trends.google.com/trends/api/dailytrends?hl=en-US&geo=US"
    raw = requests.get(url).text.lstrip(")]}',")
    data = json.loads(raw)["default"]["trendingSearchesDays"][0]["trendingSearches"]

    for item in data:
        tag = item["title"]["query"]
        delta = len(item.get("relatedQueries", [])) / 100
        velocity = item.get("traffic", 0) / 10000
        csi = (velocity * 0.7) + (delta * 0.3)

        insert_signal(
            datetime.utcnow(),
            "google_trends",
            tag,
            velocity,
            delta,
            csi,
            "consumer"
        )
