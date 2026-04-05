"""
FastAPI Tags Metadata Example (Production-Ready)

This module demonstrates:
- Organizing endpoints using OpenAPI tags
- Enhancing API documentation with metadata
- Clean and scalable API design

Use cases:
- Large microservices
- Public APIs
- ML/AI service endpoints with categorized routes
"""

from typing import List, Dict

from fastapi import FastAPI

# -------------------------------------------------------------------
# OpenAPI Tags Metadata
# -------------------------------------------------------------------

tags_metadata = [
    {
        "name": "users",
        "description": (
            "Operations related to users.\n\n"
            "Includes authentication and user management."
        ),
    },
    {
        "name": "items",
        "description": (
            "Operations for managing items.\n\n"
            "Supports CRUD and inventory-related features."
        ),
        "externalDocs": {
            "description": "Detailed Items Documentation",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

# -------------------------------------------------------------------
# FastAPI App Initialization
# -------------------------------------------------------------------

app = FastAPI(
    title="FAANG-Level API with Tags",
    description="Structured API with categorized endpoints using OpenAPI tags.",
    version="1.0.0",
    openapi_tags=tags_metadata,
)

# -------------------------------------------------------------------
# Mock Data (Replace with DB in production)
# -------------------------------------------------------------------

USERS: List[Dict[str, str]] = [
    {"name": "Harry"},
    {"name": "Ron"},
]

ITEMS: List[Dict[str, str]] = [
    {"name": "wand"},
    {"name": "flying broom"},
]

# -------------------------------------------------------------------
# Users Endpoints
# -------------------------------------------------------------------

@app.get(
    "/users/",
    tags=["users"],
    summary="Get all users",
    description="Retrieve a list of all users.",
    response_description="List of users",
)
async def get_users() -> List[Dict[str, str]]:
    """
    Fetch all users.

    Returns:
        List[Dict[str, str]]: List of user objects.
    """
    return USERS


# -------------------------------------------------------------------
# Items Endpoints
# -------------------------------------------------------------------

@app.get(
    "/items/",
    tags=["items"],
    summary="Get all items",
    description="Retrieve a list of all items.",
    response_description="List of items",
)
async def get_items() -> List[Dict[str, str]]:
    """
    Fetch all items.

    Returns:
        List[Dict[str, str]]: List of item objects.
    """
    return ITEMS