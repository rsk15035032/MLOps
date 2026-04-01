from fastapi import FastAPI
from pydantic import BaseModel


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


app = FastAPI()


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    """
    Update an item using a path parameter, request body, and optional query parameter.

    Parameters
    ----------
    item_id : int
        Unique identifier of the item to be updated (path parameter).

    item : Item
        Updated item data sent in the request body. The data must match
        the structure defined in the Item Pydantic model.

    q : str | None, optional
        Optional query parameter that can be included in the request URL.

    Returns
    -------
    dict
        A dictionary containing the item_id along with the updated item data.
        If the query parameter `q` is provided, it will also be included in
        the response.

    Example
    -------
    PUT /items/5?q=update

    Request Body:
    {
        "name": "Laptop",
        "description": "Gaming laptop",
        "price": 75000,
        "tax": 5000
    }
    """
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result