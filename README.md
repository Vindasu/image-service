# image-service

Stock image search service using Unsplash API. Returns image URLs based on search queries with configurable and custom sizes.

## Communication Contract

Uses HTTP as the communication pipe.

### How to REQUEST Data

**Endpoint:** `GET /images`

**Request Method:** HTTP GET request with query parameters

**Required Parameter:**
- `query` (string): Search term for images

**Optional Parameters:**
- `count` (integer): Number of images to return (1-30, default: 1)
- `format` (string): Image size - `raw`, `full`, `regular`, `small`, `thumb` (default: `regular`)

**Optional Dynamic Image Parameters** (Imgix transformations):
- `w` (integer): Custom width in pixels
- `h` (integer): Custom height in pixels  
- `q` (integer): Image quality (0-100, default: 80)
- `fit` (string): Fit mode - `crop`, `clip`, `scale`, `max`, `fill`
- `fmt` (string): Force image format - `jpg`, `png`, `webp`, `gif`
- `crop` (string): Crop mode - `top`, `bottom`, `left`, `right`, `faces`, `focalpoint`, `edges`, `entropy`

Learn more about supported params used in Imgix here: https://unsplash.com/documentation#supported-parameters

**Example Call (Python):**
```python
import requests

# Make request to the microservice
response = requests.get(
    "http://localhost:8000/images",
    params={
        "query": "pizza",
        "count": 3,
        "format": "small"
    }
)

# Check if request was successful
if response.status_code == 200:
    data = response.json()
    print(f"Received {len(data['images'])} images")
else:
    print(f"Error: {response.status_code}")
```

**Example Call (Python) with Dynamic Params**
```python
# Get 1920x1080 hero image, cropped to faces if present
response = requests.get(
    "http://localhost:8000/images",
    params={
        "query": "team",
        "count": 1,
        "format": "raw",
        "w": 1920,
        "h": 1080,
        "fit": "crop",
        "crop": "faces",
        "q": 95
    }
)
```

### How to RECEIVE Data

**Response Format:** JSON

**Response Structure:**
```json
{
  "images": [
    {
      "id": "string",
      "url": "string",
      "description": "string or null",
      "alt_description": "string or null"
    }
  ],
  "query": "string",
  "count": "integer",
  "format": "string"
}
```

**Success Response (200):**
```json
{
  "images": [
    {
      "id": "MQUqbmszGGM",
      "url": "https://images.unsplash.com/photo-1513104890138-7c749659a591...",
      "description": "Heavenly slice",
      "alt_description": "pizza with berries"
    },
    {
      "id": "XyZ789",
      "url": "https://images.unsplash.com/photo-1234567890...",
      "description": "Delicious pepperoni pizza",
      "alt_description": "pizza on wooden table"
    }
  ],
  "query": "pizza",
  "count": 2,
  "format": "small"
}
```

**Error Response (400 - Invalid Format):**
```json
{
  "detail": "Invalid format 'banana'. Must be one of: raw, full, regular, small, thumb"
}
```

**Error Response (422 - Missing Required Parameter):**
```json
{
  "detail": [
    {
      "loc": ["query", "query"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Example Receiving Data (Python):**
```python
import requests

response = requests.get(
    "http://localhost:8000/images",
    params={"query": "mountains", "count": 3, "format": "regular"}
)

if response.status_code == 200:
    data = response.json()
    
    # Access the images
    for image in data["images"]:
        print(f"Image ID: {image['id']}")
        print(f"URL: {image['url']}")
        print(f"Description: {image['description']}")
        print("---")
    
    # Access metadata
    print(f"\nTotal images returned: {data['count']}")
    print(f"Search query was: {data['query']}")
    print(f"Format requested: {data['format']}")
else:
    print(f"Error {response.status_code}: {response.json()['detail']}")
```

---

## UML Sequence Diagram
```
┌─────────┐          ┌───────────────────┐          ┌─────────────┐      
│  Client │          │   Image Service   │          │  Unsplash   │     
│ Program │          │   (FastAPI App)   │          │     API     │     
└────┬────┘          └─────────┬─────────┘          └──────┬──────┘          
     │                         │                           │                        
     │ GET /images?query=      │                           │                        
     │  pizza&count=3&         │                           │                        
     │  format=small           │                           │                        
     │───────────────────────> │                           │                        
     │                         │                           │                        
     │                         │ Validate parameters       │                        
     │                         │ (query, count, format)    │                        
     │                         │──┐                        │                        
     │                         │  │                        │                        
     │                         │<─┘                        │                        
     │                         │                           │                        
     │                         │ GET /search/photos?       │                        
     │                         │  query=pizza&per_page=3   │                        
     │                         │──────────────────────────>│                        
     │                         │                           │                        
     │                         │    JSON Response          │                        
     │                         │    (photo data with URLs) │                        
     │                         │<──────────────────────────│                        
     │                         │                           │                       
     │                         │ Build hotlink URLs        │                        
     │                         │ with Imgix parameters     │                        
     │                         │──┐                        │                        
     │                         │  │ For each photo:        │                        
     │                         │  │ raw_url + "&w=400&     │                        
     │                         │  │ h=300&fit=crop&q=80"   │                        
     │                         │<─┘                        │                        
     │                         │                           │                        
     │                         │ Create ImageResponse      │                        
     │                         │ with images list          │                        
     │                         │──┐                        │                        
     │                         │  │                        │                        
     │                         │<─┘                        │                        
     │                         │                           │                        
     │    JSON Response        │                           │                        
     │    200 OK               │                           │                        
     │<─────────────────────── │                           │                        
     │                         │                           │                        
     │ Parse JSON response     │                           │                       
     │ Extract image URLs      │                           │                        
     │──┐                      │                           │                        
     │  │                      │                           │                        
     │<─┘                      │                           │                        
     │                         │                           │                        

```

---

## Setup (Local)

### Prerequisites
- Python 3.8+
- Unsplash API Key

### 1. Get Unsplash API Key

1. Go to https://unsplash.com/developers
2. Sign up or login
3. Click **"New Application"**
4. Accept terms and conditions
5. Fill out the form.
6. Copy your **Access Key**

### 2. Configure Environment

Create a `.env` file in the project root:
```bash
UNSPLASH_ACCESS_KEY=your_access_key_here
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Service Locally
```bash
uvicorn app.main:app --reload
```

Service will start on: `http://localhost:8000`

## API Endpoints

### `GET /images`
Fetch images from Unsplash (see Communication Contract above)

### `GET /docs`
Interactive API documentation (Swagger UI)

