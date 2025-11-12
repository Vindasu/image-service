import requests
import json
from typing import List, Dict, Optional
from app.config import UNSPLASH_ACCESS_KEY, UNSPLASH_API

SIZES = {
    "full",
    "regular",
    "thumb",
    "small",
    "raw"
}

def get_images(query: str, count: int, format: str, dynamic: Optional[Dict] = None) -> List[Dict]:
    """
    Fetch the images from Unsplash based on query param.

    :return: list of image objects
    """
    if format not in SIZES:
        # Raise the error here that they have to provide one of the valid sizes
        raise ValueError(f"Invalid format '{format}'. Must be one of: {', '.join(SIZES)}")

    headers = {
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
    }
    url = f"{UNSPLASH_API}/search/photos"
    params = {
        "query": query,
        "per_page": count if count else 1,
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        image_data = response.json()
        photos = []
        for photo in image_data.get("results", []):
            hotlink = get_hotlink(photo, format, dynamic)

            details = {
                "id": photo.get("id"),
                "url": hotlink,
                "description": photo.get("description"),
                "alt_description": photo.get("alt_description")
            }
            photos.append(details)
        return photos

    except requests.exceptions.RequestException as e:
        raise Exception(f"Couldn't fetch images: {str(e)}")

def get_hotlink(photo: str, format: str, dynamic: Dict) -> str:
    """
    Adds all parameters for transforming the photo to request before sending to photos endpoint.
    Allows resizing, cropping, compression, and changing the format of the image.

    :return: url for dynamic image
    """
    if not dynamic:
        return photo["urls"][format if format else "regular"]

    base_url = photo["urls"]["raw"]

    params = dynamic.copy()

    if "auto" not in params:
        params["auto"] = "format"

    if "q" not in params:
        params["q"] = 80
    
    # Remove None values
    params = {k: v for k, v in params.items() if v is not None}
    
    query = "&".join([f"{k}={v}" for k, v in params.items()])
    
    return f"{base_url}&{query}"

    




