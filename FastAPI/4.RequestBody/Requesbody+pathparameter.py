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
async def update_item(item_id: int, item: Item):
    """
    Update an existing item using a path parameter and request body.

    Parameters
    ----------
    item_id : int
        Unique identifier of the item to be updated (path parameter).

    item : Item
        Updated item data sent in the request body. The data must match
        the structure defined in the Item Pydantic model.

    Returns
    -------
    dict
        A dictionary containing the item_id along with the updated item data.

    Example
    -------
    PUT /items/10

    Request Body:
    {
        "name": "Laptop",
        "description": "Gaming laptop",
        "price": 80000,
        "tax": 5000
    }
    """
    return {"item_id": item_id, **item.model_dump()}