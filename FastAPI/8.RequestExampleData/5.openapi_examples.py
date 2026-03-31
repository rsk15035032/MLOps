from typing import Annotated

from fastapi import Body, FastAPI
from pydantic import BaseModel

# Create FastAPI application
app = FastAPI()


class Item(BaseModel):
    """
    Item Model

    This model defines the structure of the request body.
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
    *,
    item_id: int,
    item: Annotated[
        Item,
        Body(
            # Advanced Swagger examples using OpenAPI format
            openapi_examples={

                # Example 1 → Fully valid request
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2,
                    },
                },

                # Example 2 → FastAPI automatically converts string to float
                "converted": {
                    "summary": "An example with converted data",
                    "description": "FastAPI can convert price `strings` to actual `numbers` automatically.",
                    "value": {
                        "name": "Bar",
                        "price": "35.4",
                    },
                },

                # Example 3 → Invalid example (shows validation error)
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "name": "Baz",
                        "price": "thirty five point four",
                    },
                },
            },
        ),
    ],
):
    """
    Update Item API using OpenAPI Examples

    This endpoint demonstrates the most advanced way to add
    request body examples in FastAPI using `openapi_examples`.

    Why this is important
    ---------------------
    Unlike simple examples, OpenAPI examples allow:
    - Multiple examples
    - Summary for each example
    - Description for each example
    - Valid and invalid request demonstrations

    This makes Swagger documentation more professional
    and easier for developers to understand.

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
        A dictionary containing the item ID and updated item data.

    Example Endpoint
    ----------------
    PUT /items/10
    """

    results = {"item_id": item_id, "item": item}
    return results