from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    """
    Retrieve an item by its ID.

    This endpoint accepts an integer item ID as a path parameter
    and returns the same ID in JSON format. It is a simple example
    that demonstrates how FastAPI handles path parameters with
    type validation.

    Args:
        item_id (int): The unique identifier of the item.

    Returns:
        dict: A JSON response containing the provided item ID.

    Example:
        GET /items/25

        Response:
        {
            "item_id": 25
        }
    """
    return {"item_id": item_id}