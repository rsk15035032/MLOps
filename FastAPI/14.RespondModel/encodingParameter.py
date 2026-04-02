from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    """
    Represents an item in the system.

    Attributes:
        name (str): The name of the item.
        description (str | None): Optional description providing more details about the item.
        price (float): The price of the item.
        tax (float): Tax applied to the item. Defaults to 10.5 if not provided.
        tags (list[str]): List of tags associated with the item (e.g., categories or labels).
    """
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []


# In-memory "database" (mock data for demonstration purposes)
items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {
        "name": "Bar",
        "description": "The bartenders",
        "price": 62,
        "tax": 20.2,
    },
    "baz": {
        "name": "Baz",
        "description": None,
        "price": 50.2,
        "tax": 10.5,
        "tags": [],
    },
}


@app.get(
    "/items/{item_id}",
    response_model=Item,
    response_model_exclude_unset=True
)
async def read_item(item_id: str):
    """
    Retrieve an item by its ID.

    This endpoint fetches an item from the in-memory data store
    and returns it as a validated `Item` response model.

    Args:
        item_id (str): The unique identifier of the item.

    Returns:
        Item: The item data matching the given ID.

    Raises:
        KeyError: If the item_id does not exist in the data store.

    Notes:
        - `response_model=Item` ensures response validation and serialization.
        - `response_model_exclude_unset=True` excludes fields that were not
          explicitly set in the stored data (e.g., default values like tax or tags).
    """
    return items[item_id]