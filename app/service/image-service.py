import requests
from typing import List, Dict
from app.config import UNSPLASH_ACCESS_KEY, UNSPLASH_API

SIZES = {
    "thumbnail": {"w": 200, "h": 200},
    "card": {"w": 400, "h": 300},
    "banner": {"w": 1200, "h": 400},
    "hero": {"w": 1920, "h": 1080},
    "regular": {}
}

def get_images(query: str, count: int, format: str) -> List[Dict]:
    """
    
    """