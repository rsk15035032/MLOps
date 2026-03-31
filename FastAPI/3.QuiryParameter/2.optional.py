from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


"""
    Retrieve an item by its ID with an optional query parameter.

    This endpoint demonstrates how to use:
    1. Path parameters
    2. Optional query parameters
    3. Conditional responses in FastAPI

    Parameters
    ----------
    item_id : str
        A required path parameter that represents the ID of the item.
        It is passed directly in the URL.

    q : str | None, optional (default = None)
        An optional query parameter.
        If provided, it will be included in the response.
        If not provided, only the item_id will be returned.

    Example Requests
    ----------------
    /items/123
    /items/123?q=phone
    /items/abc?q=fastapi

    Example Responses
    -----------------
    If q is provided:
        {"item_id": "123", "q": "phone"}

    If q is NOT provided:
        {"item_id": "123"}

    Returns
    -------
    dict
        A JSON response containing the item ID and optionally the query value.
    """
