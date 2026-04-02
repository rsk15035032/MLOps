from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class BaseItem(BaseModel):
    """
    Base schema for all item types.

    Attributes:
        description (str): Description of the item.
        type (str): Type identifier used to distinguish item categories.
    """
    description: str
    type: str


class CarItem(BaseItem):
    """
    Schema representing a car item.

    Defaults:
        type (str): Always set to "car".
    """
    type: str = "car"


class PlaneItem(BaseItem):
    """
    Schema representing a plane item.

    Attributes:
        size (int): Size of the plane.
    
    Defaults:
        type (str): Always set to "plane".
    """
    type: str = "plane"
    size: int


# In-memory data store (mock database)
items = {
    "item1": {
        "description": "All my friends drive a low rider",
        "type": "car",
    },
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}


@app.get("/items/{item_id}", response_model=PlaneItem | CarItem)
async def read_item(item_id: str):
    """
    Retrieve an item by ID with dynamic response model.

    This endpoint returns different schemas based on the item type:
        - CarItem if type == "car"
        - PlaneItem if type == "plane"

    Args:
        item_id (str): Unique identifier of the item.

    Returns:
        PlaneItem | CarItem: Item data validated against one of the models.

    Note:
        FastAPI will automatically determine which model to use
        based on the returned data structure.
    """
    return items[item_id]  # Direct access (raises KeyError if not found)