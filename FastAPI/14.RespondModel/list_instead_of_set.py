from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    """
    Data model representing an item.

    Attributes:
        name (str): Name of the item.
        description (str | None): Optional description of the item.
        price (float): Price of the item.
        tax (float): Tax applied to the item (default is 10.5).
    """
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5


# In-memory data store (mock database)
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
    response_model_include=["name", "description"],  # Only include these fields
)
async def read_item_name(item_id: str):
    """
    Retrieve only the name and description of a specific item.

    Args:
        item_id (str): Unique identifier of the item.

    Returns:
        dict: Item data containing only 'name' and 'description'.
    """
    return items[item_id]  # Direct access (raises KeyError if item_id not found)


@app.get(
    "/items/{item_id}/public",
    response_model=Item,
    response_model_exclude=["tax"],  # Exclude tax from response
)
async def read_item_public_data(item_id: str):
    """
    Retrieve public-facing data of an item excluding the tax field.

    Args:
        item_id (str): Unique identifier of the item.

    Returns:
        dict: Item data without the 'tax' field.
    """
    return items[item_id]  # Direct access (raises KeyError if item_id not found)