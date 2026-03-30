from fastapi import FastAPI
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


class User(BaseModel):
    """
    Pydantic model representing a user.

    Attributes
    ----------
    username : str
        Username of the user.

    full_name : str | None, optional
        Full name of the user. Default is None.
    """
    username: str
    full_name: str | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    """
    Update an item using a path parameter and multiple request body models.

    This endpoint demonstrates how FastAPI can accept multiple objects
    in the request body (e.g., an Item and a User) at the same time.

    Parameters
    ----------
    item_id : int
        Unique identifier of the item to be updated (path parameter).

    item : Item
        Item data sent in the request body.

    user : User
        User data sent in the request body.

    Returns
    -------
    dict
        A dictionary containing the item_id along with the item and user data.

    Example
    -------
    PUT /items/10

    Request Body:
    {
        "item": {
            "name": "Laptop",
            "description": "Gaming laptop",
            "price": 70000,
            "tax": 5000
        },
        "user": {
            "username": "ravi123",
            "full_name": "Ravi Kumar"
        }
    }
    """
    results = {"item_id": item_id, "item": item, "user": user}
    return results