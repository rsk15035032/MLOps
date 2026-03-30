from typing import Annotated

from fastapi import FastAPI, Path
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    """
    Pydantic model representing an item.

    Attributes
    ----------
    name : str
        Name of the item.

    description : str | None, optional
        Description of the item. Default is None.

    price : float
        Price of the item.

    tax : float | None, optional
        Tax value for the item. Default is None.
    """
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str | None = None,
    item: Item | None = None,
):
    """
    Update an item using a validated path parameter, optional query parameter,
    and optional request body.

    This endpoint demonstrates how to use `Annotated` with `Path` to apply
    validation constraints (minimum and maximum values) to a path parameter.

    Parameters
    ----------
    item_id : int
        Unique identifier of the item. The value must be between 0 and 1000
        (inclusive), as defined using Path validation.

    q : str | None, optional
        Optional query parameter that can be included in the request URL.

    item : Item | None, optional
        Optional item data sent in the request body. If provided, it must match
        the structure defined in the Item Pydantic model.

    Returns
    -------
    dict
        A dictionary containing the item_id. If query parameter `q` is provided,
        it will be included in the response. If item data is provided in the
        request body, it will also be included in the response.

    Example
    -------
    PUT /items/10?q=test

    Request Body:
    {
        "name": "Laptop",
        "description": "Gaming laptop",
        "price": 70000,
        "tax": 5000
    }
    """
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results