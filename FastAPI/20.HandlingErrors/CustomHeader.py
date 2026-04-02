from fastapi import FastAPI, HTTPException

app = FastAPI()

# In-memory data store (simulating a simple database)
items = {"foo": "The Foo Wrestlers"}


@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    """
    Retrieve an item by its ID with custom error headers.

    This endpoint attempts to fetch an item from the in-memory `items` dictionary.
    If the item exists, it returns the item data.
    If the item does not exist, it raises an HTTP 404 exception and includes
    a custom response header for additional error context.

    Args:
        item_id (str): The unique identifier of the item to retrieve.

    Returns:
        dict: A dictionary containing the requested item.

    Raises:
        HTTPException:
            - 404 Not Found: If the item_id does not exist.
              Includes a custom header "X-Error" for debugging or client handling.

    Example:
        Request:
            GET /items-header/foo

        Response:
            {
                "item": "The Foo Wrestlers"
            }

        Error Response:
            Status Code: 404
            Headers:
                X-Error: There goes my error
            Body:
            {
                "detail": "Item not found"
            }
    """

    # Check if the requested item exists
    if item_id not in items:
        # Raise HTTP 404 with a custom header for additional context
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )

    # Return the item if found
    return {"item": items[item_id]}