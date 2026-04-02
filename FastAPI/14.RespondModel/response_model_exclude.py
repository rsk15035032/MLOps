from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    """
    Represents an item entity.

    Attributes:
        name (str): Name of the item.
        description (str | None): Optional description of the item.
        price (float): Price of the item.
        tax (float): Tax applied to the item (default = 10.5).
    """
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5


# Mock database
items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}


@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"},
)
async def read_item_name(item_id: str):
    """
    Retrieve only the name and description of an item.

    Args:
        item_id (str): Unique identifier of the item.

    Returns:
        dict: Contains only 'name' and 'description' fields.

    Raises:
        HTTPException: If the item is not found.
    """
    item = items.get(item_id)

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return item


@app.get(
    "/items/{item_id}/public",
    response_model=Item,
    response_model_exclude={"tax"},
)
async def read_item_public_data(item_id: str):
    """
    Retrieve public-facing item data excluding sensitive fields.

    Args:
        item_id (str): Unique identifier of the item.

    Returns:
        dict: Item data without the 'tax' field.

    Raises:
        HTTPException: If the item is not found.
    """
    item = items.get(item_id)

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return item