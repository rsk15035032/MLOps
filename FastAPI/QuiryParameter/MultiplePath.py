
"""
    Retrieve a specific item that belongs to a specific user.

    This endpoint demonstrates:
    1. Multiple path parameters
    2. Optional query parameters
    3. Boolean query parameters
    4. Dynamic response building using a dictionary

    Path Parameters
    ---------------
    user_id : int
        Required path parameter representing the unique ID of the user.

    item_id : str
        Required path parameter representing the unique ID of the item
        that belongs to the user.

    Query Parameters
    ----------------
    q : str | None, optional (default = None)
        Optional query parameter.
        If provided, it will be added to the response.

    short : bool, optional (default = False)
        Controls whether the full description should be returned.
        - short = True  -> Only basic item details are returned
        - short = False -> A long description is included

    How it works
    ------------
    1. A dictionary is created with item_id and owner_id (user_id).
    2. If the query parameter 'q' is provided, it is added to the response.
    3. If 'short' is False, a long description is added.
    4. The final dictionary is returned as a JSON response.

    Example Requests
    ----------------
    /users/1/items/101
    /users/1/items/101?q=phone
    /users/1/items/101?short=true
    /users/1/items/101?q=phone&short=true

    Example Responses
    -----------------
    /users/1/items/101
        {"item_id": "101", "owner_id": 1, "description": "This is an amazing item that has a long description"}

    /users/1/items/101?q=phone
        {"item_id": "101", "owner_id": 1, "q": "phone", "description": "This is an amazing item that has a long description"}

    /users/1/items/101?short=true
        {"item_id": "101", "owner_id": 1}

    Returns
    -------
    dict
        A JSON response containing item details along with the user (owner) ID.
"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item