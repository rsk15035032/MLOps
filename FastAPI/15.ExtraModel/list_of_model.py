from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    """
    Schema representing an item.

    Attributes:
        name (str): Name of the item.
        description (str): Description of the item.
    """
    name: str
    description: str


# In-memory list acting as a mock database
items = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]


@app.get("/items/", response_model=list[Item])
async def read_items():
    """
    Retrieve all items.

    Returns:
        list[Item]: A list of items validated against the Item schema.

    Note:
        FastAPI automatically:
        - Validates each dictionary in the list
        - Converts them into Item objects
        - Ensures consistent response structure
    """
    return items