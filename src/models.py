"""Pydantic models for Parent Phone SOS."""

from typing import Optional, List
from pydantic import BaseModel, Field


class Coordinates(BaseModel):
    """Coordinates of a UI element."""

    x: int = Field(..., description="X coordinate in pixels")
    y: int = Field(..., description="Y coordinate in pixels")
    width: int = Field(..., description="Width in pixels")
    height: int = Field(..., description="Height in pixels")


class Step(BaseModel):
    """Single instruction step."""

    step_number: int = Field(..., description="Step number (1-indexed)")
    instruction_text: str = Field(..., description="What the user should do")
    ui_element: str = Field(..., description="Name of the UI element to interact with")
    coordinates: Optional[Coordinates] = Field(
        None, description="Location of the UI element on screen"
    )


class AnalysisResult(BaseModel):
    """Result from AI analysis of a screenshot."""

    summary: str = Field(..., description="Brief description of the solution")
    steps: List[Step] = Field(..., description="Step-by-step instructions")
    difficulty: str = Field(
        ..., description="Difficulty level: easy, medium, or hard"
    )
    estimated_time: int = Field(..., description="Estimated time in minutes")
    provider: str = Field(..., description="AI provider used (openai or anthropic)")


class AnalyzeRequest(BaseModel):
    """Request to analyze a screenshot."""

    question: str = Field(..., description="What problem needs to be solved?")


class FAQItem(BaseModel):
    """FAQ item."""

    id: str = Field(..., description="Unique identifier")
    category: str = Field(..., description="Category name in Chinese")
    category_en: str = Field(..., description="Category name in English")
    steps: List[str] = Field(..., description="Solution steps")
    platforms: List[str] = Field(
        ..., description="Applicable platforms: iPhone, Android, WeChat, etc."
    )


class FAQResponse(BaseModel):
    """Response with FAQ data."""

    items: List[FAQItem] = Field(..., description="List of FAQ items")
    count: int = Field(..., description="Total number of items")
