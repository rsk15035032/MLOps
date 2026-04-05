"""
FastAPI Static Files Configuration (Production-Ready)

This module demonstrates how to:
- Serve static files (CSS, JS, images)
- Mount a static directory safely
- Use configurable paths for flexibility

Use cases:
- Frontend assets (React, Vue builds)
- ML dashboards (charts, UI)
- Documentation hosting
"""

from pathlib import Path
import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# -------------------------------------------------------------------
# Logging Configuration
# -------------------------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------------------------------------------------
# FastAPI App Initialization
# -------------------------------------------------------------------

app = FastAPI(title="Static Files API")

# -------------------------------------------------------------------
# Static Directory Configuration
# -------------------------------------------------------------------

STATIC_DIR = Path("static")

# Validate static directory exists
if not STATIC_DIR.exists():
    logger.warning(f"Static directory not found: {STATIC_DIR.resolve()}")
    # Optionally create it (safer in dev environments)
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    logger.info(f"Created missing static directory: {STATIC_DIR.resolve()}")

# -------------------------------------------------------------------
# Mount Static Files
# -------------------------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static",
)

# -------------------------------------------------------------------
# Health Check Endpoint
# -------------------------------------------------------------------

@app.get("/")
async def root():
    """
    Health check endpoint.

    Returns:
        dict: API status.
    """
    return {"status": "running"}