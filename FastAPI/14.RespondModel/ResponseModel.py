from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    """
    Pydantic model representing an item.

    This model is used for:
    - Request body validation
    - Response model validation
    """

    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Any:
    """
    Create a new item.

    The request body is validated using the Item model.
    The response is also validated using response_model=Item.

    Parameters
    ----------
    item : Item
        Item data sent in the request body

    Returns
    -------
    Item
        The validated item
    """

    return item


@app.get("/items/", response_model=list[Item])
async def read_items() -> Any:
    """
    Retrieve a list of items.

    Even though we return dictionaries, FastAPI automatically:
    - Converts them into Item objects
    - Validates the response using the Item model

    Returns
    -------
    list[Item]
        List of validated items
    """

    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]