from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    """
    Item model used for request and response validation.

    Attributes
    ----------
    name : str
        Name of the item (required)

    description : str | None
        Optional description of the item

    price : float
        Price of the item (required)

    tax : float | None
        Optional tax value

    tags : list[str]
        List of tags related to the item
    """

    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []


@app.post("/items/")
async def create_item(item: Item) -> Item:
    """
    Create a new item.

    This endpoint accepts an item in the request body,
    validates it using the Item model, and returns the same item.

    Parameters
    ----------
    item : Item
        Item data received in the request body

    Returns
    -------
    Item
        The validated item
    """

    # Return the validated item
    return item


@app.get("/items/")
async def read_items() -> list[Item]:
    """
    Retrieve a list of items.

    This endpoint returns a list of predefined items
    using the Item model as the response type.

    Returns
    -------
    list[Item]
        List of items
    """

    # Return sample items
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]