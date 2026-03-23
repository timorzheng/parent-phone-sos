"""AI Screenshot Analyzer using OpenAI GPT-4o Vision or Claude Vision."""

import base64
import json
import logging
from typing import Optional
from io import BytesIO

from PIL import Image
import httpx

from src.config import settings
from src.models import AnalysisResult, Step, Coordinates
from src.prompts import SYSTEM_PROMPT, SYSTEM_PROMPT_ANTHROPIC, USER_PROMPT_TEMPLATE

logger = logging.getLogger(__name__)


def encode_image_to_base64(image: Image.Image) -> str:
    """Encode PIL Image to base64 string."""
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return base64.standard_b64encode(buffer.getvalue()).decode("utf-8")


def analyze_screenshot_openai(
    image: Image.Image, question: str
) -> Optional[AnalysisResult]:
    """Analyze screenshot using OpenAI GPT-4o Vision API."""
    if not settings.OPENAI_API_KEY:
        logger.warning("OpenAI API key not configured")
        return None

    try:
        image_base64 = encode_image_to_base64(image)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        }

        payload = {
            "model": settings.OPENAI_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": SYSTEM_PROMPT},
                        {
                            "type": "text",
                            "text": USER_PROMPT_TEMPLATE.format(question=question),
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_base64}",
                                "detail": "high",
                            },
                        },
                    ],
                }
            ],
            "max_tokens": 2000,
            "temperature": 0.3,
        }

        with httpx.Client() as client:
            response = client.post(
                "https://api.openai.com/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=60.0,
            )
            response.raise_for_status()

        result = response.json()
        content = result["choices"][0]["message"]["content"]

        # Parse JSON response
        analysis_data = json.loads(content)

        # Convert to AnalysisResult model
        steps = [
            Step(
                step_number=s["step_number"],
                instruction_text=s["instruction_text"],
                ui_element=s["ui_element"],
                coordinates=(
                    Coordinates(**s["coordinates"]) if s.get("coordinates") else None
                ),
            )
            for s in analysis_data.get("steps", [])
        ]

        return AnalysisResult(
            summary=analysis_data.get("summary", ""),
            steps=steps,
            difficulty=analysis_data.get("difficulty", "medium"),
            estimated_time=analysis_data.get("estimated_time", 5),
            provider="openai",
        )

    except Exception as e:
        logger.error(f"OpenAI analysis failed: {e}")
        return None


def analyze_screenshot_anthropic(
    image: Image.Image, question: str
) -> Optional[AnalysisResult]:
    """Analyze screenshot using Anthropic Claude Vision API."""
    if not settings.ANTHROPIC_API_KEY:
        logger.warning("Anthropic API key not configured")
        return None

    try:
        image_base64 = encode_image_to_base64(image)
        image_size = image.size

        headers = {
            "x-api-key": settings.ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }

        payload = {
            "model": settings.ANTHROPIC_MODEL,
            "max_tokens": 2000,
            "system": SYSTEM_PROMPT_ANTHROPIC,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": image_base64,
                            },
                        },
                        {
                            "type": "text",
                            "text": USER_PROMPT_TEMPLATE.format(question=question),
                        },
                    ],
                }
            ],
        }

        with httpx.Client() as client:
            response = client.post(
                "https://api.anthropic.com/v1/messages",
                json=payload,
                headers=headers,
                timeout=60.0,
            )
            response.raise_for_status()

        result = response.json()
        content = result["content"][0]["text"]

        # Parse JSON response
        analysis_data = json.loads(content)

        # Convert to AnalysisResult model
        steps = [
            Step(
                step_number=s["step_number"],
                instruction_text=s["instruction_text"],
                ui_element=s["ui_element"],
                coordinates=(
                    Coordinates(**s["coordinates"]) if s.get("coordinates") else None
                ),
            )
            for s in analysis_data.get("steps", [])
        ]

        return AnalysisResult(
            summary=analysis_data.get("summary", ""),
            steps=steps,
            difficulty=analysis_data.get("difficulty", "medium"),
            estimated_time=analysis_data.get("estimated_time", 5),
            provider="anthropic",
        )

    except Exception as e:
        logger.error(f"Anthropic analysis failed: {e}")
        return None


def analyze_screenshot(
    image: Image.Image, question: str, provider: Optional[str] = None
) -> Optional[AnalysisResult]:
    """
    Analyze a screenshot using AI.

    Args:
        image: PIL Image object
        question: User's question/problem description
        provider: Preferred provider ('openai' or 'anthropic'). If None, uses settings.PREFERRED_PROVIDER

    Returns:
        AnalysisResult or None if analysis fails
    """
    if not provider:
        provider = settings.PREFERRED_PROVIDER

    logger.info(f"Starting analysis with provider: {provider}")

    if provider == "openai":
        result = analyze_screenshot_openai(image, question)
        if result:
            return result
        # Fallback to Anthropic if OpenAI fails
        logger.info("OpenAI failed, falling back to Anthropic")
        return analyze_screenshot_anthropic(image, question)

    else:  # anthropic or fallback
        result = analyze_screenshot_anthropic(image, question)
        if result:
            return result
        # Fallback to OpenAI if Anthropic fails
        logger.info("Anthropic failed, falling back to OpenAI")
        return analyze_screenshot_openai(image, question)
