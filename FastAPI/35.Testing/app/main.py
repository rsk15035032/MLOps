"""
FastAPI Items API (Production-Ready)

This module demonstrates:
- Header-based authentication using dependency injection
- CRUD operations with validation
- Clean architecture for scalability

Features:
- Reusable auth dependency
- Structured error handling
- Pydantic v2 compatibility
"""

from typing import Annotated, Dict

from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel

# -------------------------------------------------------------------
# App Initialization
# -------------------------------------------------------------------

app = FastAPI(title="Items API")

# -------------------------------------------------------------------
# Constants & Mock DB
# -------------------------------------------------------------------

FAKE_SECRET_TOKEN = "coneofsilence"

fake_db: Dict[str, Dict] = {
    "foo": {"id": "foo", "title": "Foo", "description": "There goes my hero"},
    "bar": {"id": "bar", "title": "Bar", "description": "The bartenders"},
}

# -------------------------------------------------------------------
# Models
# -------------------------------------------------------------------

class Item(BaseModel):
    """
    Represents an item entity.

    Attributes:
        id (str): Unique identifier.
        title (str): Item title.
        description (str | None): Optional description.
    """
    id: str
    title: str
    description: str | None = None


# -------------------------------------------------------------------
# Dependencies
# -------------------------------------------------------------------

def verify_token(x_token: Annotated[str, Header()]) -> str:
    """
    Validate X-Token header.

    Args:
        x_token (str): Token from request header.

    Returns:
        str: Validated token.

    Raises:
        HTTPException: If token is invalid.
    """
    if x_token != FAKE_SECRET_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid X-Token header",
        )
    return x_token


# -------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------

@app.get(
    "/items/{item_id}",
    response_model=Item,
    summary="Get item by ID",
)
async def read_item(
    item_id: str,
    _: Annotated[str, Depends(verify_token)],  # Auth dependency
) -> Item:
    """
    Retrieve an item by its ID.

    Args:
        item_id (str): Item identifier.

    Returns:
        Item: Requested item.

    Raises:
        HTTPException:
            - 404 if item not found
    """
    if item_id not in fake_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    return fake_db[item_id]


@app.post(
    "/items/",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new item",
)
async def create_item(
    item: Item,
    _: Annotated[str, Depends(verify_token)],  # Auth dependency
) -> Item:
    """
    Create a new item.

    Args:
        item (Item): Item payload.

    Returns:
        Item: Created item.

    Raises:
        HTTPException:
            - 409 if item already exists
    """
    if item.id in fake_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Item already exists",
        )

    fake_db[item.id] = item.model_dump()
    return item