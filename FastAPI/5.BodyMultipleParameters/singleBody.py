from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    """
    Request body schema for an item.

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
    """
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    """
    Update an item using an embedded request body.

    This endpoint demonstrates how to use `Body(embed=True)` so that the
    request body must be wrapped inside a key named "item".

    Example request body:
    {
        "item": {
            "name": "Laptop",
            "description": "Gaming laptop",
            "price": 75000,
            "tax": 5000
        }
    }

    Parameters
    ----------
    item_id : int
        Unique ID of the item (passed as a path parameter).
    item : Item
        Item object embedded inside the request body using `Body(embed=True)`.

    Returns
    -------
    dict
        A dictionary containing the item ID and the updated item data.
    """
    results = {"item_id": item_id, "item": item}
    return results