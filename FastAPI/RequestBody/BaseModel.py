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
        Short description of the item. Default is None.

    price : float
        Price of the item.

    tax : float | None, optional
        Tax applied to the item. Default is None.
    """
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    """
    Create a new item using a request body.

    Parameters
    ----------
    item : Item
        Item data sent in the request body as JSON. The data must match
        the structure defined in the Item Pydantic model.

    Returns
    -------
    Item
        The same item data that was sent in the request body.

    Example
    -------
    POST /items/

    Request Body:
    {
        "name": "Laptop",
        "description": "Gaming laptop",
        "price": 75000,
        "tax": 5000
    }
    """
    return item