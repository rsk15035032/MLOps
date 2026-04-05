"""
FastAPI Custom Documentation Configuration

This module demonstrates how to:
- Customize Swagger UI documentation path
- Disable ReDoc
- Build clean, production-ready API configuration

Use cases:
- Internal APIs (custom docs URL)
- Secured environments (hide default docs)
- API gateway integrations
"""

from fastapi import FastAPI
from typing import List, Dict

# -------------------------------------------------------------------
# FastAPI App Initialization
# -------------------------------------------------------------------

app = FastAPI(
    title="Custom Docs API",
    description="API with customized Swagger UI and disabled ReDoc.",
    version="1.0.0",
    docs_url="/documentation",  # ✅ Custom Swagger UI path
    redoc_url=None,            # ❌ Disable ReDoc
    openapi_url="/openapi.json",  # Explicit OpenAPI schema path
)

# -------------------------------------------------------------------
# Mock Data
# -------------------------------------------------------------------

ITEMS: List[Dict[str, str]] = [
    {"name": "Foo"},
]

# -------------------------------------------------------------------
# API Endpoints
# -------------------------------------------------------------------

@app.get(
    "/items/",
    summary="Get all items",
    description="Retrieve a list of items.",
    response_description="List of items",
)
async def read_items() -> List[Dict[str, str]]:
    """
    Fetch all items.

    Returns:
        List[Dict[str, str]]: A list of item objects.
    """
    return ITEMS