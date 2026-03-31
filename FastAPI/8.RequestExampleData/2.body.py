from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel

# Create FastAPI application
app = FastAPI()


class Item(BaseModel):
    """
    Item Model

    This model represents the structure of the request body.
    FastAPI uses this model to validate incoming JSON data
    and automatically generate API documentation.

    Attributes
    ----------
    name : str
        Name of the item.
    description : str | None
        Optional description of the item.
    price : float
        Price of the item.
    tax : float | None
        Optional tax value.
    """

    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Annotated[
        Item,
        Body(
            examples=[
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        ),
    ],
):
    """
    Update Item API using Annotated + Body Examples

    This endpoint demonstrates how to add request body examples
    using the modern FastAPI approach: Annotated + Body().

    Why this is important
    ---------------------
    Instead of adding examples inside the model,
    we are adding them directly to the request body.

    This gives more flexibility when:
    - The same model is used in multiple APIs
    - Each API needs a different example
    - You want better control over Swagger documentation

    Parameters
    ----------
    item_id : int
        ID of the item provided in the URL.

    item : Item
        Request body containing item details.
        The example provided inside Body() will automatically
        appear in Swagger UI.

    Returns
    -------
    dict
        A dictionary containing the item ID and updated item data.

    Example Request
    ---------------
    PUT /items/10

    {
        "name": "Foo",
        "description": "A very nice Item",
        "price": 35.4,
        "tax": 3.2
    }
    """

    results = {"item_id": item_id, "item": item}
    return results