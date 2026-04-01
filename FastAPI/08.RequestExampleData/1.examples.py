from fastapi import FastAPI
from pydantic import BaseModel

# Create FastAPI application
app = FastAPI()


class Item(BaseModel):
    """
    Item Model

    This model represents an item that will be updated using the API.

    This example also demonstrates how to add a custom example
    that will automatically appear in Swagger UI.

    How it works
    ------------
    FastAPI uses Pydantic to generate the API schema.
    By using 'json_schema_extra', we can manually provide
    example data that Swagger will display.

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

    # This configuration is used to customize the JSON schema
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    """
    Update Item API

    This endpoint updates an item using:
    1. Path parameter (item_id)
    2. Request body (Item model)

    The example defined inside the Item model will automatically
    appear in Swagger UI when you click "Try it out".

    Parameters
    ----------
    item_id : int
        ID of the item provided in the URL.
    item : Item
        Item data received in the request body.

    Returns
    -------
    dict
        A dictionary containing the item ID and updated item details.
    """

    results = {"item_id": item_id, "item": item}
    return results