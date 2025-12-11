import requests
from datetime import datetime
from utils.db import insert_signal

def run():
    url = "https://steamspy.com/api.php?request=genre"   # example endpoint
    data = requests.get(url).json()

    for genre, metrics in data.items():
        velocity = float(metrics.get("score", 0)) / 100
        delta = float(metrics.get("games", 0)) / 1000
        csi = (velocity + delta) / 2

        insert_signal(
            datetime.utcnow(),
            "steam_spy",
            genre,
            velocity,
            delta,
            csi,
            "gaming"
        )
