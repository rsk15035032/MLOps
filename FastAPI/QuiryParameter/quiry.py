from fastapi import FastAPI

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

"""
    Retrieve a list of items using pagination.

    This endpoint returns items from a fake database (a simple Python list).
    It demonstrates how query parameters work in FastAPI.

    Query Parameters
    ----------------
    skip : int, optional (default = 0)
        Number of items to skip from the beginning of the list.
        Useful when implementing pagination.

    limit : int, optional (default = 10)
        Maximum number of items to return.

    How it works
    ------------
    Python slicing is used to return a portion of the list:

        fake_items_db[skip : skip + limit]

    Example Requests
    ----------------
    /items/                  -> Returns all items
    /items/?skip=1           -> Skips the first item
    /items/?skip=1&limit=1   -> Returns only one item after skipping one

    Returns
    -------
    list
        A list of items from the fake database based on skip and limit.
    """