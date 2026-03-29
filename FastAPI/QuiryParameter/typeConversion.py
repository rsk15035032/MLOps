
"""
    Retrieve an item by ID with optional query parameters.

    This endpoint demonstrates:
    1. Path parameters (item_id)
    2. Optional query parameters (q)
    3. Boolean query parameters (short)
    4. How to dynamically modify the response

    Parameters
    ----------
    item_id : str
        Required path parameter that represents the unique ID of the item.

    q : str | None, optional (default = None)
        Optional query parameter.
        If provided, it will be added to the response.

    short : bool, optional (default = False)
        Boolean query parameter used to control the response.
        - If short = True  -> Only basic item information is returned
        - If short = False -> A long description is included

    How it works
    ------------
    1. First, a dictionary with item_id is created.
    2. If the user provides 'q', it is added using item.update().
    3. If 'short' is False, a long description is added to the response.

    Example Requests
    ----------------
    /items/1
    /items/1?q=phone
    /items/1?short=true
    /items/1?q=phone&short=true

    Example Responses
    -----------------
    /items/1
        {"item_id": "1", "description": "This is an amazing item that has a long description"}

    /items/1?q=phone
        {"item_id": "1", "q": "phone", "description": "This is an amazing item that has a long description"}

    /items/1?short=true
        {"item_id": "1"}

    Returns
    -------
    dict
        A JSON response containing the item information with optional fields.
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item