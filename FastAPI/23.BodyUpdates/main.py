from fastapi import FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, field_validator
from typing import Dict, Optional, List

app = FastAPI()


class Item(BaseModel):
    """
    Represents an item in the system.

    Attributes:
        name (Optional[str]): Name of the item.
        description (Optional[str]): Detailed description of the item.
        price (Optional[float]): Price of the item (must be > 0 if provided).
        tax (float): Tax applied to the item. Defaults to 10.5.
        tags (List[str]): List of tags associated with the item.
    """

    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: float = 10.5
    tags: List[str] = Field(default_factory=list)

    @field_validator("price")
    @classmethod
    def validate_price(cls, value: Optional[float]) -> Optional[float]:
        """
        Validates that the price, if provided, is greater than zero.

        Args:
            value (Optional[float]): The price to validate.

        Returns:
            Optional[float]: The validated price.

        Raises:
            ValueError: If price is less than or equal to zero.
        """
        if value is not None and value <= 0:
            raise ValueError("Price must be greater than 0")
        return value


# Simulated in-memory database
items: Dict[str, dict] = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
async def read_item(item_id: str) -> Item:
    """
    Retrieve a single item by its ID.

    Args:
        item_id (str): Unique identifier of the item.

    Returns:
        Item: The requested item.

    Raises:
        HTTPException: If the item is not found.
    """
    if item_id not in items:
        # Raise 404 error if item does not exist
        raise HTTPException(status_code=404, detail="Item not found")

    return items[item_id]


@app.patch("/items/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
async def update_item(item_id: str, item: Item) -> Item:
    """
    Partially update an existing item.

    This endpoint supports PATCH semantics:
    - Only fields explicitly provided in the request will be updated.
    - Existing fields remain unchanged if not provided.

    Args:
        item_id (str): Unique identifier of the item.
        item (Item): Partial item data to update.

    Returns:
        Item: The updated item.

    Raises:
        HTTPException: If the item is not found.
    """
    if item_id not in items:
        # Raise 404 error if item does not exist
        raise HTTPException(status_code=404, detail="Item not found")

    # Retrieve existing item data
    stored_item_data = items[item_id]

    # Convert stored data into a Pydantic model
    stored_item_model = Item(**stored_item_data)

    # Extract only fields that were provided in the request
    update_data = item.model_dump(exclude_unset=True)

    # Create updated model by merging old data with new data
    updated_item = stored_item_model.model_copy(update=update_data)

    # Convert to JSON-compatible format for storage
    items[item_id] = jsonable_encoder(updated_item)

    return updated_item