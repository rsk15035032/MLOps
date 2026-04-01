from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl
from typing import Optional, Set

app = FastAPI()


class Image(BaseModel):
    """
    Represents an image associated with an item.

    This model is used as a nested request body inside the Item model.

    Attributes
    ----------
    url : HttpUrl
        A valid image URL. Automatically validated by Pydantic.
    name : str
        Name of the image.
    """
    url: HttpUrl
    name: str


class Item(BaseModel):
    """
    Represents an item that will be updated through the API.

    This model demonstrates:
    - Required fields (name, price)
    - Optional fields (description, tax, image)
    - Default values (tags)
    - Nested models (Image)

    Attributes
    ----------
    name : str
        Name of the item.
    description : Optional[str]
        Description of the item.
    price : float
        Price of the item.
    tax : Optional[float]
        Optional tax value.
    tags : Set[str]
        A set of unique tags associated with the item.
    image : Optional[Image]
        Optional nested image object.
    """
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = set()
    image: Optional[Image] = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    """
    Update an item using a path parameter and request body.

    FastAPI automatically:
    - Reads JSON data from the request body
    - Validates it using the Item model
    - Converts it into a Python object

    Parameters
    ----------
    item_id : int
        ID of the item provided in the URL.
    item : Item
        Item data received in the request body.

    Returns
    -------
    dict
        A dictionary containing the item ID and updated item data.
    """
    results = {"item_id": item_id, "item": item}
    return results