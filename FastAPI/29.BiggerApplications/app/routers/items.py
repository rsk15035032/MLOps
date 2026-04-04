from fastapi import APIRouter, Depends, HTTPException

from ..dependencies import get_token_header

# -------------------------------------------------------------------
# Router Configuration
# -------------------------------------------------------------------

router = APIRouter(
    prefix="/items",  # Base path for all item-related endpoints
    tags=["items"],   # Default tag for grouping in API docs
    dependencies=[Depends(get_token_header)],  # Apply auth dependency globally
    responses={404: {"description": "Not found"}},  # Default 404 response
)

# -------------------------------------------------------------------
# In-Memory Database (Mock Data)
# -------------------------------------------------------------------

fake_items_db = {
    "plumbus": {"name": "Plumbus"},
    "gun": {"name": "Portal Gun"}
}


# -------------------------------------------------------------------
# Endpoints
# -------------------------------------------------------------------

@router.get("/")
async def read_items():
    """
    Retrieve all items.

    This endpoint returns all items from the in-memory database.
    Access is protected by a header-based token dependency.

    Returns:
        dict: A dictionary containing all available items
    """
    return fake_items_db


@router.get("/{item_id}")
async def read_item(item_id: str):
    """
    Retrieve a specific item by its ID.

    Args:
        item_id (str): Unique identifier of the item

    Raises:
        HTTPException: If the item is not found in the database

    Returns:
        dict: Item details including its name and ID
    """
    if item_id not in fake_items_db:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return {
        "name": fake_items_db[item_id]["name"],
        "item_id": item_id
    }


@router.put(
    "/{item_id}",
    tags=["custom"],  # Overrides default tag for this route
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    """
    Update a specific item.

    This endpoint demonstrates restricted update logic.
    Only the item with ID 'plumbus' can be updated.

    Args:
        item_id (str): Unique identifier of the item

    Raises:
        HTTPException:
            - 403 if the update is not allowed
            - 404 handled by router default response config

    Returns:
        dict: Updated item information
    """
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403,
            detail="You can only update the item: plumbus"
        )

    return {
        "item_id": item_id,
        "name": "The great Plumbus"
    }