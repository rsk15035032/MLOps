from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    """
    Schema for the item that will be updated.

    Attributes
    ----------
    name : str
        Name of the item.
    description : str | None, optional
        Optional description of the item.
    price : float
        Price of the item.
    tax : float | None, optional
        Optional tax applied to the item.
    """
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    """
    Schema representing the user who is updating the item.

    Attributes
    ----------
    username : str
        Username of the user.
    full_name : str | None, optional
        Full name of the user.
    """
    username: str
    full_name: str | None = None


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item,
    user: User,
    importance: Annotated[int, Body(gt=0)],
    q: str | None = None,
):
    """
    Update an existing item using multiple request body parameters.

    Parameters
    ----------
    item_id : int
        Unique identifier of the item to update (passed in the path).
    item : Item
        Item data containing name, description, price, and tax.
    user : User
        User information who is performing the update.
    importance : int
        Importance level of the update. Must be greater than 0.
    q : str | None, optional
        Optional query string parameter.

    Returns
    -------
    dict
        A dictionary containing the updated item information along with user
        details and importance level.
    """
    results = {
        "item_id": item_id,
        "item": item,
        "user": user,
        "importance": importance,
    }

    if q:
        results.update({"q": q})

    return results