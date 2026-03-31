from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

# Create FastAPI application
app = FastAPI()


class Image(BaseModel):
    """
    Image Model

    This model represents an image that belongs to an item.

    FastAPI uses Pydantic models to:
    - Validate incoming JSON data
    - Convert JSON into Python objects
    - Automatically generate API documentation (Swagger UI)

    Attributes
    ----------
    url : HttpUrl
        A valid image URL. Pydantic automatically checks whether
        the URL is valid or not (must start with http:// or https://).

    name : str
        Name of the image.
    """

    url: HttpUrl   # URL must be valid
    name: str      # Name of the image


class Item(BaseModel):
    """
    Item Model (Main Request Body)

    This model represents an item that will be updated using the API.

    Concepts used in this model
    ---------------------------
    1. Required fields
       Fields like 'name' and 'price' are required because they
       do not have default values.

    2. Optional fields
       Fields like 'description', 'tax', and 'images' are optional.
       The user is not required to send them in the request body.

    3. List of nested models
       The 'images' field is a list of Image objects.
       This means the request body must contain a list of objects.

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

    tags : set[str]
        A set of unique tags related to the item.

    images : list[Image] | None
        A list of image objects.
    """

    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    """
    Update Item API

    This endpoint updates an item using:
    1. Path parameter (item_id)
    2. Request body (Item model)

    How this works internally
    -------------------------
    - FastAPI reads the JSON request body
    - Converts it into the Item model
    - Validates all fields (price must be float, URL must be valid, etc.)
    - Passes the validated object to this function

    Parameters
    ----------
    item_id : int
        The ID of the item provided in the URL.
        Example: /items/5

    item : Item
        The request body containing item data.
        FastAPI automatically converts JSON into a Python object.

    Returns
    -------
    dict
        A dictionary containing the item ID and updated item details.

    Example Request
    ---------------
    PUT /items/5

    {
      "name": "Laptop",
      "description": "Gaming laptop",
      "price": 80000,
      "tax": 2000,
      "tags": ["electronics", "gaming"],
      "images": [
        {
          "url": "https://example.com/laptop1.png",
          "name": "Front View"
        },
        {
          "url": "https://example.com/laptop2.png",
          "name": "Back View"
        }
      ]
    }

    Example Response
    ----------------
    {
      "item_id": 5,
      "item": {
        "name": "Laptop",
        "description": "Gaming laptop",
        "price": 80000,
        "tax": 2000,
        "tags": ["electronics", "gaming"],
        "images": [
          {
            "url": "https://example.com/laptop1.png",
            "name": "Front View"
          },
          {
            "url": "https://example.com/laptop2.png",
            "name": "Back View"
          }
        ]
      }
    }
    """

    # Combine path parameter and request body into a single response
    results = {
        "item_id": item_id,
        "item": item
    }

    return results