from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id):
    """
    Retrieve an item using its ID.

    This endpoint accepts an item ID as a path parameter and
    returns it in JSON format. It is commonly used as a basic
    example to demonstrate how path parameters work in FastAPI.

    Args:
        item_id (int or str): The unique identifier of the item.

    Returns:
        dict: A JSON response containing the provided item ID.

    Example:
        GET /items/10
        Response:
        {
            "item_id": 10
        }
    """
    return {"item_id": item_id}


