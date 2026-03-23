"""Tests for the annotation engine."""

import pytest
from PIL import Image
from src.models import AnalysisResult, Step, Coordinates
from src.annotator import (
    annotate_screenshot,
    save_annotated_image,
    image_to_bytes,
    get_best_font_size,
    get_contrasting_color,
)


@pytest.fixture
def sample_image():
    """Create a sample image for testing."""
    img = Image.new("RGB", (800, 600), color=(255, 255, 255))
    return img


@pytest.fixture
def sample_analysis():
    """Create a sample analysis result for testing."""
    return AnalysisResult(
        summary="Test analysis",
        steps=[
            Step(
                step_number=1,
                instruction_text="Tap the WiFi button",
                ui_element="WiFi Settings",
                coordinates=Coordinates(x=100, y=100, width=80, height=40),
            ),
            Step(
                step_number=2,
                instruction_text="Select your network",
                ui_element="Network List",
                coordinates=Coordinates(x=200, y=200, width=100, height=50),
            ),
        ],
        difficulty="easy",
        estimated_time=5,
        provider="test",
    )


def test_get_best_font_size():
    """Test font size calculation."""
    assert get_best_font_size(800) > 0
    assert get_best_font_size(400) > 0
    assert get_best_font_size(800) > get_best_font_size(400)


def test_get_contrasting_color(sample_image):
    """Test contrasting color detection."""
    # Light background should return dark color
    light_img = Image.new("RGB", (800, 600), color=(200, 200, 200))
    color = get_contrasting_color(light_img, 400, 300)
    assert isinstance(color, tuple)
    assert len(color) == 3


def test_annotate_screenshot(sample_image, sample_analysis):
    """Test screenshot annotation."""
    annotated = annotate_screenshot(sample_image, sample_analysis)

    # Check result is an image
    assert isinstance(annotated, Image.Image)

    # Check dimensions are preserved
    assert annotated.width == sample_image.width
    assert annotated.height == sample_image.height

    # Check it's RGB
    assert annotated.mode == "RGB"


def test_image_to_bytes(sample_image):
    """Test image to bytes conversion."""
    image_bytes = image_to_bytes(sample_image, format="PNG")

    assert isinstance(image_bytes, bytes)
    assert len(image_bytes) > 0

    # Check it's a valid PNG
    assert image_bytes[:4] == b"\x89PNG"


def test_save_annotated_image(sample_image, tmp_path):
    """Test saving annotated image to file."""
    output_path = tmp_path / "test_output.png"

    result = save_annotated_image(sample_image, str(output_path), format="PNG")

    assert result is True
    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_annotate_with_no_coordinates(sample_image):
    """Test annotation with steps that have no coordinates."""
    analysis = AnalysisResult(
        summary="Test",
        steps=[
            Step(
                step_number=1,
                instruction_text="Do something",
                ui_element="Some element",
                coordinates=None,
            )
        ],
        difficulty="easy",
        estimated_time=1,
        provider="test",
    )

    # Should not raise an error
    annotated = annotate_screenshot(sample_image, analysis)
    assert isinstance(annotated, Image.Image)
