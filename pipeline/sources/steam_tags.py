import requests
from datetime import datetime
from utils.db import insert_signal

def run():
    url = "https://steamspy.com/api.php?request=top100in2weeks"  # Get top 100 games for better data
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to fetch Steam data: {response.status_code}")
        return
    
    data = response.json()
    
    # Process top games and use their names as tags
    for app_id, game_data in data.items():
        # Extract meaningful metrics
        positive = float(game_data.get("positive", 0))
        negative = float(game_data.get("negative", 0))
        ccu = float(game_data.get("ccu", 0))
        owners = game_data.get("owners", "0 .. 0")
        
        # Calculate velocity based on positive reviews ratio
        total_reviews = positive + negative
        velocity = (positive / total_reviews * 100) if total_reviews > 0 else 0
        
        # Calculate delta based on current concurrent users
        delta = ccu / 1000  # Normalize by 1000
        
        # Calculate CSI (Consumer Sentiment Index)
        csi = (velocity * 0.6) + (delta * 0.4)
        
        # Use game name as the tag (cleaned for database)
        game_name = game_data.get("name", f"Game_{app_id}").strip()
        
        insert_signal(
            datetime.utcnow(),
            "steam_spy",
            game_name,
            velocity,
            delta,
            csi,
            "gaming"
        )
