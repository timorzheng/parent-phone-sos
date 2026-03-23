"""Image annotation engine using Pillow."""

import logging
from typing import Optional, Tuple
from PIL import Image, ImageDraw, ImageFont

from src.models import AnalysisResult

logger = logging.getLogger(__name__)

# Color constants
RED = (255, 50, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def get_best_font_size(image_width: int) -> int:
    """Calculate appropriate font size based on image width."""
    return max(20, image_width // 30)


def get_contrasting_color(image: Image.Image, x: int, y: int) -> Tuple[int, int, int]:
    """Determine if the area is light or dark and return contrasting color."""
    try:
        # Sample a region around the point
        sample_size = 20
        x1 = max(0, x - sample_size)
        y1 = max(0, y - sample_size)
        x2 = min(image.width, x + sample_size)
        y2 = min(image.height, y + sample_size)

        sampled = image.crop((x1, y1, x2, y2))
        avg_color = sampled.convert("RGB").resize((1, 1)).getpixel((0, 0))

        # Calculate brightness
        brightness = (avg_color[0] * 299 + avg_color[1] * 587 + avg_color[2] * 114) / 1000

        # If bright area, use dark color; if dark area, use light color
        return WHITE if brightness > 128 else RED
    except Exception as e:
        logger.warning(f"Could not determine contrasting color: {e}")
        return RED


def draw_circle(draw: ImageDraw.ImageDraw, x: int, y: int, radius: int, color: Tuple[int, int, int], width: int = 3):
    """Draw a circle outline."""
    draw.ellipse([x - radius, y - radius, x + radius, y + radius], outline=color, width=width)


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    x1: int,
    y1: int,
    x2: int,
    y2: int,
    color: Tuple[int, int, int],
    width: int = 3,
):
    """Draw an arrow pointing from (x1,y1) to (x2,y2)."""
    import math

    # Draw line
    draw.line([(x1, y1), (x2, y2)], fill=color, width=width)

    # Draw arrowhead
    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_size = 15

    # Arrow tip
    tip_x = x2 - arrow_size * math.cos(angle)
    tip_y = y2 - arrow_size * math.sin(angle)

    # Arrow points
    left_x = tip_x - arrow_size * math.cos(angle + math.pi / 6)
    left_y = tip_y - arrow_size * math.sin(angle + math.pi / 6)

    right_x = tip_x - arrow_size * math.cos(angle - math.pi / 6)
    right_y = tip_y - arrow_size * math.sin(angle - math.pi / 6)

    draw.polygon([(x2, y2), (left_x, left_y), (right_x, right_y)], fill=color)


def add_step_number(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    step_num: int,
    font: Optional[ImageFont.FreeTypeFont] = None,
    color: Tuple[int, int, int] = RED,
):
    """Add a numbered step label (①②③ format)."""
    # Unicode circled numbers
    circled_nums = "①②③④⑤⑥⑦⑧⑨⑩"
    num_text = circled_nums[min(step_num - 1, len(circled_nums) - 1)]

    bbox = draw.textbbox((0, 0), num_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Draw text with shadow for better visibility
    shadow_offset = 2
    draw.text((x - text_width // 2 + shadow_offset, y - text_height // 2 + shadow_offset), num_text, fill=BLACK, font=font)
    draw.text((x - text_width // 2, y - text_height // 2), num_text, fill=color, font=font)


def annotate_screenshot(
    image: Image.Image,
    analysis: AnalysisResult,
) -> Image.Image:
    """
    Annotate screenshot with analysis results.

    Args:
        image: PIL Image to annotate
        analysis: AnalysisResult containing steps with coordinates

    Returns:
        Annotated PIL Image
    """
    # Create a copy to avoid modifying original
    annotated = image.copy().convert("RGB")
    draw = ImageDraw.Draw(annotated)

    # Calculate font size
    font_size = get_best_font_size(image.width)

    # Try to load a nice font, fallback to default
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except (OSError, IOError):
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except (OSError, IOError):
            font = ImageFont.load_default()

    # Draw annotations for each step
    for step in analysis.steps:
        if not step.coordinates:
            continue

        coords = step.coordinates
        x, y = coords.x + coords.width // 2, coords.y + coords.height // 2

        # Determine best color for visibility
        element_color = get_contrasting_color(annotated, x, y)

        # Draw circle around UI element
        radius = max(coords.width, coords.height) // 2 + 10
        draw_circle(draw, x, y, radius, RED, width=4)

        # Draw arrow from circle to step number
        arrow_end_x = x + radius + 40
        arrow_end_y = y - radius - 40
        draw_arrow(draw, x + radius, y, arrow_end_x, arrow_end_y, RED, width=3)

        # Draw step number
        add_step_number(draw, arrow_end_x, arrow_end_y, step.step_number, font, RED)

    logger.info(f"Screenshot annotated with {len(analysis.steps)} steps")
    return annotated


def save_annotated_image(image: Image.Image, output_path: str, format: str = "PNG") -> bool:
    """
    Save annotated image to file.

    Args:
        image: PIL Image to save
        output_path: Path to save to
        format: Image format (PNG, JPEG)

    Returns:
        True if successful
    """
    try:
        image.save(output_path, format=format)
        logger.info(f"Annotated image saved to {output_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to save annotated image: {e}")
        return False


def image_to_bytes(image: Image.Image, format: str = "PNG") -> bytes:
    """Convert PIL Image to bytes."""
    from io import BytesIO

    buffer = BytesIO()
    image.save(buffer, format=format)
    buffer.seek(0)
    return buffer.getvalue()
