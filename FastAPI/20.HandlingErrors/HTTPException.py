from fastapi import FastAPI, HTTPException

app = FastAPI()

# In-memory data store (simulating a database)
items = {"foo": "The Foo Wrestlers"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    """
    Retrieve an item by its ID.

    This endpoint searches for an item in the in-memory `items` dictionary.
    If the item exists, it returns the item data.
    If the item does not exist, it raises an HTTP 404 exception.

    Args:
        item_id (str): The unique identifier of the item to retrieve.

    Returns:
        dict: A dictionary containing the requested item.

    Raises:
        HTTPException: 
            - 404 Not Found: If the item_id does not exist in the data store.

    Example:
        Request:
            GET /items/foo

        Response:
            {
                "item": "The Foo Wrestlers"
            }
    """

    # Check if the item exists in the dictionary
    if item_id not in items:
        # Raise a 404 error if item is not found
        raise HTTPException(status_code=404, detail="Item not found")

    # Return the requested item
    return {"item": items[item_id]}