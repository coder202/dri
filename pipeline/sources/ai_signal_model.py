from datetime import datetime

try:
    from utils.db import insert_signal
except Exception:
    def insert_signal(*args, **kwargs):
        pass

def run():
    tags = {
        "procedural-roguelike": 0.072,
        "tactical-coop-builder": 0.055,
        "grimdark-survival": 0.089
    }

    for tag, csi in tags.items():
        velocity = csi * 0.5
        delta = csi * 0.25

        insert_signal(
            datetime.utcnow(),
            "ai_model",
            tag,
            velocity,
            delta,
            csi,
            "future-signals"
        )
