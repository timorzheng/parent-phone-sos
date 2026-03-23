"""Tests for the FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient
from PIL import Image
from io import BytesIO

from src.main import app

client = TestClient(app)


@pytest.fixture
def sample_image_file():
    """Create a sample image file for upload."""
    img = Image.new("RGB", (400, 300), color=(255, 255, 255))
    img_io = BytesIO()
    img.save(img_io, format="PNG")
    img_io.seek(0)
    return img_io


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert "service" in data
    assert "version" in data


def test_api_info():
    """Test API info endpoint."""
    response = client.get("/api/info")
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Parent Phone SOS"
    assert "version" in data
    assert "providers" in data
    assert "max_image_size_mb" in data


def test_faq_list():
    """Test FAQ list endpoint."""
    response = client.get("/api/faq/list")
    assert response.status_code == 200

    data = response.json()
    assert "items" in data
    assert "count" in data
    assert data["count"] > 0
    assert len(data["items"]) > 0


def test_faq_get_item():
    """Test get specific FAQ item."""
    # Get list first to find a valid ID
    list_response = client.get("/api/faq/list")
    items = list_response.json()["items"]

    if items:
        item_id = items[0]["id"]
        response = client.get(f"/api/faq/{item_id}")
        assert response.status_code == 200

        data = response.json()
        assert data["id"] == item_id
        assert "category" in data
        assert "steps" in data


def test_faq_not_found():
    """Test FAQ item not found."""
    response = client.get("/api/faq/nonexistent")
    assert response.status_code == 404


def test_faq_search():
    """Test FAQ search endpoint."""
    response = client.get("/api/faq/search?q=wifi")
    assert response.status_code == 200

    data = response.json()
    assert "items" in data
    assert "count" in data


def test_faq_search_too_short():
    """Test FAQ search with too short query."""
    response = client.get("/api/faq/search?q=a")
    assert response.status_code == 400


def test_analyze_missing_file():
    """Test analyze endpoint without file."""
    response = client.post("/api/analyze", data={"question": "Test question"})
    assert response.status_code == 422  # Unprocessable Entity


def test_analyze_missing_question(sample_image_file):
    """Test analyze endpoint without question."""
    response = client.post(
        "/api/analyze",
        files={"file": ("test.png", sample_image_file, "image/png")},
    )
    assert response.status_code == 422


def test_analyze_invalid_format():
    """Test analyze with invalid file format."""
    response = client.post(
        "/api/analyze",
        files={"file": ("test.txt", BytesIO(b"not an image"), "text/plain")},
        data={"question": "Test question"},
    )
    assert response.status_code == 415


@pytest.mark.skip(reason="Requires API key configuration")
def test_analyze_valid_request(sample_image_file):
    """Test analyze with valid request (skipped without API key)."""
    response = client.post(
        "/api/analyze",
        files={"file": ("test.png", sample_image_file, "image/png")},
        data={"question": "How do I connect to WiFi?"},
    )

    # This would need valid API keys to run
    if response.status_code == 200:
        data = response.json()
        assert "analysis" in data
        assert "annotated_image_base64" in data
