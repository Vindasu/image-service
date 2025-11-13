import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint returns service info"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "image service"
    assert data["status"] == "running"
    assert "endpoints" in data

def test_images_endpoint_success():
    """Test fetching images with valid parameters"""
    response = client.get("/images?query=pizza&count=2&format=regular")
    assert response.status_code == 200
    
    data = response.json()
    assert "images" in data
    assert "query" in data
    assert "count" in data
    assert "format" in data
    
    assert data["query"] == "pizza"
    assert data["format"] == "regular"
    assert len(data["images"]) <= 2  # May be less if Unsplash has fewer results
    
    # Check image structure
    if len(data["images"]) > 0:
        image = data["images"][0]
        assert "id" in image
        assert "url" in image
        assert image["url"].startswith("https://")

def test_images_endpoint_invalid_format():
    """Test that invalid format returns 400 error"""
    response = client.get("/images?query=pizza&format=invalid")
    assert response.status_code == 400
    assert "Invalid format" in response.json()["detail"]

def test_images_endpoint_missing_query():
    """Test that missing query parameter returns 422 error"""
    response = client.get("/images?count=1&format=regular")
    assert response.status_code == 422  # Validation error

def test_images_count_validation():
    """Test count parameter validation (1-30)"""
    # Too low
    response = client.get("/images?query=test&count=0")
    assert response.status_code == 422
    
    # Too high
    response = client.get("/images?query=test&count=31")
    assert response.status_code == 422
    
    # Valid
    response = client.get("/images?query=test&count=5")
    assert response.status_code == 200

def test_all_format_sizes():
    """Test all supported format sizes"""
    formats = ["raw", "full", "regular", "small", "thumb"]
    
    for format_type in formats:
        response = client.get(f"/images?query=sunset&count=1&format={format_type}")
        assert response.status_code == 200, f"Failed for format: {format_type}"
        data = response.json()
        assert data["format"] == format_type

def test_image_subject_search():
    """
    Search for an image by subject.
    """
    response = client.get("/images?query=ocean&count=1&format=regular")
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "ocean"
    assert len(data["images"]) > 0

def test_image_formatting():
    """
    Receive images in requested format.
    """
    response = client.get("/images?query=mountain&count=1&format=thumb")
    assert response.status_code == 200
    data = response.json()
    assert data["format"] == "thumb"
    assert len(data["images"]) > 0
    
    # Verify it's actually an image URL
    assert data["images"][0]["url"].startswith("https://")

def test_image_options_reliability():
    """
    Receive multiple images.
    """
    response = client.get("/images?query=pizza&count=3&format=regular")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["images"]) <= 3
    assert data["count"] == len(data["images"])