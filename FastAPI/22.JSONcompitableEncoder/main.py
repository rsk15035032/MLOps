from datetime import datetime

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

# Simulated in-memory database
fake_db = {}


class Item(BaseModel):
    """
    Data model representing an item.

    Attributes:
        title (str): The title of the item.
        timestamp (datetime): The date and time associated with the item.
        description (str | None): Optional description of the item.
    """

    title: str
    timestamp: datetime
    description: str | None = None


app = FastAPI()


@app.put("/items/{id}")
def update_item(id: str, item: Item):
    """
    Create or update an item in the database.

    This endpoint receives an item as input, converts it into a JSON-compatible
    format, and stores it in the in-memory database using the provided ID.

    The `jsonable_encoder` is used to ensure that complex data types
    (like datetime) are converted into JSON-serializable formats.

    Args:
        id (str): The unique identifier for the item.
        item (Item): The item data received in the request body.

    Returns:
        dict: The stored item data in JSON-compatible format.

    Example:
        Request:
            PUT /items/1
            {
                "title": "Learn FastAPI",
                "timestamp": "2026-04-03T10:00:00",
                "description": "Study FastAPI deeply"
            }

        Response:
            {
                "title": "Learn FastAPI",
                "timestamp": "2026-04-03T10:00:00",
                "description": "Study FastAPI deeply"
            }
    """

    # Convert Pydantic model to JSON-compatible dict
    # (e.g., datetime -> ISO string)
    json_compatible_item_data = jsonable_encoder(item)

    # Store or update the item in the fake database
    fake_db[id] = json_compatible_item_data

    # Return the stored data
    return json_compatible_item_data