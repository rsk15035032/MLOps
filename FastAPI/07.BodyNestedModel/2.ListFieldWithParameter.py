from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    """
    Pydantic model representing an item with a list of tags.

    Attributes
    ----------
    name : str
        Name of the item.
    description : str | None, optional
        Optional description of the item.
    price : float
        Price of the item.
    tax : float | None, optional
        Optional tax value.
    tags : list[str], optional
        List of tags associated with the item.
    """
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    """
    Update an item using a request body that includes a list of strings.

    This endpoint demonstrates:
    - Path parameters
    - Request body validation using Pydantic
    - List fields using modern Python typing (list[str])

    Example Request Body
    --------------------
    {
        "name": "Laptop",
        "description": "Gaming laptop",
        "price": 75000,
        "tax": 5000,
        "tags": ["electronics", "gaming", "laptop"]
    }

    Parameters
    ----------
    item_id : int
        Unique identifier of the item (path parameter).
    item : Item
        Item object containing name, price, and a list of tags.

    Returns
    -------
    dict
        A dictionary containing the item ID and the updated item data.
    """
    results = {"item_id": item_id, "item": item}
    return results