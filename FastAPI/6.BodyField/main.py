from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    """
    Pydantic model representing an item with validation rules.

    Attributes
    ----------
    name : str
        Name of the item.
    description : str | None, optional
        Description of the item (maximum 300 characters).
    price : float
        Price of the item. Must be greater than 0.
    tax : float | None, optional
        Optional tax value applied to the item.
    """
    name: str
    description: str | None = Field(
        default=None,
        title="The description of the item",
        max_length=300
    )
    price: float = Field(
        gt=0,
        description="The price must be greater than zero"
    )
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    """
    Update an item using a validated request body.

    This endpoint demonstrates:
    - Path parameters
    - Pydantic model validation using Field()
    - Embedded request body using Body(embed=True)

    Example Request Body
    --------------------
    {
        "item": {
            "name": "Laptop",
            "description": "High-performance gaming laptop",
            "price": 75000,
            "tax": 5000
        }
    }

    Parameters
    ----------
    item_id : int
        Unique identifier of the item (path parameter).
    item : Item
        Item object validated using Pydantic Field() constraints.

    Returns
    -------
    dict
        A dictionary containing the item ID and the validated item data.
    """
    results = {"item_id": item_id, "item": item}
    return results