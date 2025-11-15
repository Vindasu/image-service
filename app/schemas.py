# This holds the data interfaces for the request and response bodies

from pydantic import BaseModel
from typing import List, Optional

class ImageRequest(BaseModel):
    query: str
    count: Optional[int] = 1
    format: Optional[str] = "regular"

class ImageData(BaseModel):
    id: str
    url: str
    description: Optional[str]
    alt_description: Optional[str]

class ImageResponse(BaseModel):
    images: List[ImageData]
    query: str
    count: int
    format: str