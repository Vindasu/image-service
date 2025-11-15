from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import ImageResponse, ImageData
from app.service.unsplash import get_images, SIZES

app = FastAPI(    
    title="image service",
    description="Fetch stock images from Unsplash API",
    version="1.0.0"
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specify domains when deployed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "service": "image service",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "images": "/images",
            "docs": "/docs"
        }
    }


@app.get("/images", response_model=ImageResponse)
def fetch_images(
    query: str = Query(..., description="Search term (e.g., 'pizza', 'sunset')"),
    count: int = Query(1, ge=1, le=30, description="Number of images (1-30)"),
    format: str = Query("regular", description=f"Image size: {', '.join(SIZES)}"),
    dynamic: dict = Query(None, description="Dynamic image parameters")
):
    """
    Fetch images from Unsplash based on search query.
    """
    
    try:
        images_data = get_images(query, count, format, dynamic)
        
        # Convert to Pydantic models
        images = [ImageData(**img) for img in images_data]
        
        return ImageResponse(
            images=images,
            query=query,
            count=len(images),
            format=format
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
