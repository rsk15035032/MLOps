from fastapi import FastAPI
from pydantic import BaseModel, Field

# Create FastAPI application
app = FastAPI()


class Item(BaseModel):
    """
    Item Model with Field-Level Examples

    This model demonstrates how to use Pydantic's Field() function
    to add examples for each field individually.

    These examples automatically appear in Swagger UI and help users
    understand what kind of data they should send in the request body.

    Attributes
    ----------
    name : str
        Name of the item.
        Example shown in Swagger: "Foo"

    description : str | None
        Optional description of the item.
        Example shown in Swagger: "A very nice Item"

    price : float
        Price of the item.
        Example shown in Swagger: 35.4

    tax : float | None
        Optional tax value.
        Example shown in Swagger: 3.2
    """

    name: str = Field(examples=["Foo"])
    description: str | None = Field(default=None, examples=["A very nice Item"])
    price: float = Field(examples=[35.4])
    tax: float | None = Field(default=None, examples=[3.2])


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    """
    Update Item API

    This endpoint updates an item using:
    1. A path parameter (item_id)
    2. A request body (Item model)

    FastAPI automatically:
    - Reads JSON data from the request body
    - Validates it using the Item model
    - Shows examples in Swagger based on Field(examples=...)

    Parameters
    ----------
    item_id : int
        ID of the item provided in the URL.
    item : Item
        Item data received in the request body.

    Returns
    -------
    dict
        A dictionary containing the item ID and the updated item data.
    """

    results = {"item_id": item_id, "item": item}
    return results