"""FastAPI backend for Parent Phone SOS."""

import logging
import os
from io import BytesIO
from typing import Optional
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import uvicorn

from src.config import settings
from src.models import AnalyzeRequest, AnalysisResult, FAQResponse
from src.analyzer import analyze_screenshot
from src.annotator import annotate_screenshot, image_to_bytes
from src.faq import get_all_faq, get_faq_by_id, search_faq

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Parent Phone SOS",
    description="AI-powered remote phone support for parents",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the directory where this file is located
BASE_DIR = Path(__file__).resolve().parent.parent

# Mount static files
web_dir = BASE_DIR / "web"
if web_dir.exists():
    app.mount("/", StaticFiles(directory=str(web_dir), html=True), name="web")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "Parent Phone SOS",
        "version": "0.1.0",
    }


@app.post("/api/analyze")
async def analyze(
    file: UploadFile = File(...),
    question: str = Form(...),
    provider: Optional[str] = Form(None),
):
    """
    Analyze a screenshot and return step-by-step instructions with annotation.

    Args:
        file: Screenshot image file
        question: Description of the problem
        provider: Preferred AI provider (openai or anthropic)

    Returns:
        JSON with analysis result and annotated image
    """
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="File is required")

        # Check file size
        file_content = await file.read()
        file_size_mb = len(file_content) / (1024 * 1024)
        if file_size_mb > settings.MAX_IMAGE_SIZE_MB:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Max size: {settings.MAX_IMAGE_SIZE_MB}MB",
            )

        # Validate file type
        file_ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
        if file_ext not in settings.ALLOWED_IMAGE_FORMATS:
            raise HTTPException(
                status_code=415,
                detail=f"Unsupported file format. Allowed: {', '.join(settings.ALLOWED_IMAGE_FORMATS)}",
            )

        # Open image
        try:
            image = Image.open(BytesIO(file_content))
            if image.mode == "RGBA":
                # Convert RGBA to RGB for compatibility
                rgb_image = Image.new("RGB", image.size, (255, 255, 255))
                rgb_image.paste(image, mask=image.split()[3] if len(image.split()) > 3 else None)
                image = rgb_image
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")

        logger.info(f"Processing screenshot: {file.filename}, Question: {question}")

        # Analyze screenshot
        analysis = analyze_screenshot(image, question, provider)

        if not analysis:
            raise HTTPException(
                status_code=500,
                detail="Failed to analyze image. Please try again or provide a clearer screenshot.",
            )

        logger.info(f"Analysis successful: {len(analysis.steps)} steps identified")

        # Annotate image
        try:
            annotated_image = annotate_screenshot(image, analysis)
            annotated_bytes = image_to_bytes(annotated_image, format="PNG")
        except Exception as e:
            logger.warning(f"Annotation failed: {e}")
            annotated_bytes = None

        # Return response
        response_data = {
            "analysis": analysis.model_dump(),
            "annotated_image_base64": None,
        }

        if annotated_bytes:
            import base64

            response_data["annotated_image_base64"] = base64.b64encode(annotated_bytes).decode("utf-8")

        return JSONResponse(content=response_data)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during analysis: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/faq/list")
async def get_faq_list():
    """Get list of all FAQ categories."""
    try:
        faq_items = get_all_faq()
        return FAQResponse(
            items=faq_items,
            count=len(faq_items),
        )
    except Exception as e:
        logger.error(f"Error fetching FAQ list: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch FAQ list")


@app.get("/api/faq/{faq_id}")
async def get_faq_item(faq_id: str):
    """Get a specific FAQ item by ID."""
    try:
        item = get_faq_by_id(faq_id)
        if not item:
            raise HTTPException(status_code=404, detail="FAQ item not found")
        return item
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching FAQ item: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch FAQ item")


@app.get("/api/faq/search")
async def search_faq_endpoint(q: str):
    """Search FAQ by keyword."""
    try:
        if not q or len(q) < 2:
            raise HTTPException(status_code=400, detail="Search term must be at least 2 characters")

        results = search_faq(q)
        return FAQResponse(
            items=results,
            count=len(results),
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching FAQ: {e}")
        raise HTTPException(status_code=500, detail="Failed to search FAQ")


@app.get("/api/info")
async def get_api_info():
    """Get API information."""
    return {
        "name": "Parent Phone SOS",
        "version": "0.1.0",
        "description": "AI-powered remote phone support for parents",
        "providers": ["openai", "anthropic"],
        "max_image_size_mb": settings.MAX_IMAGE_SIZE_MB,
        "allowed_formats": settings.ALLOWED_IMAGE_FORMATS,
    }


@app.get("/")
async def root():
    """Redirect to web UI."""
    return FileResponse(web_dir / "index.html")


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info" if not settings.DEBUG else "debug",
    )
