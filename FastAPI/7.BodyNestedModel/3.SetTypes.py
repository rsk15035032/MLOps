from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    """
    Pydantic model representing an item with a set of tags.

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
    tags : set[str], optional
        A set of tags associated with the item.
        Duplicate values are automatically removed.
    """
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    """
    Update an item using a request body that includes a set of strings.

    This endpoint demonstrates:
    - Path parameters
    - Request body validation using Pydantic
    - Use of `set[str]` to automatically remove duplicate tags

    Example Request Body
    --------------------
    {
        "name": "Laptop",
        "description": "Gaming laptop",
        "price": 75000,
        "tax": 5000,
        "tags": ["electronics", "gaming", "gaming", "laptop"]
    }

    After validation, the duplicate value will be removed automatically.

    Parameters
    ----------
    item_id : int
        Unique identifier of the item (path parameter).
    item : Item
        Item object containing name, price, and a set of tags.

    Returns
    -------
    dict
        A dictionary containing the item ID and the updated item data.
    """
    results = {"item_id": item_id, "item": item}
    return results