from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel

# Create FastAPI application
app = FastAPI()


class Item(BaseModel):
    """
    Item Model

    This model defines the structure of the request body.
    FastAPI uses this model to validate the incoming JSON data
    and automatically generate Swagger documentation.

    Attributes
    ----------
    name : str
        Name of the item.
    description : str | None
        Optional description of the item.
    price : float
        Price of the item (must be a valid float).
    tax : float | None
        Optional tax value.
    """

    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Annotated[
        Item,
        Body(
            examples=[
                # Example 1 → Fully valid request
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },

                # Example 2 → Valid but minimal request
                # (description and tax are optional)
                {
                    "name": "Bar",
                    "price": 35.4,
                },

                # Example 3 → Invalid example (used to show validation error)
                # Here price is not a number
                {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            ],
        ),
    ],
):
    """
    Update Item API using Multiple Request Body Examples

    This endpoint demonstrates how to add multiple examples
    for the same request body using Annotated + Body().

    Why this is useful
    ------------------
    Multiple examples help API users understand:
    1. A complete valid request
    2. A minimal valid request
    3. An invalid request that will trigger validation errors

    The '*' in the function parameters makes sure that
    all parameters must be passed as keyword arguments.

    Parameters
    ----------
    item_id : int
        ID of the item provided in the URL path.

    item : Item
        Request body containing item data.
        FastAPI validates this using the Pydantic model.

    Returns
    -------
    dict
        A dictionary containing the item ID and the validated item data.

    Example Endpoint
    ----------------
    PUT /items/10
    """

    results = {"item_id": item_id, "item": item}
    return results