"""
    Retrieve an item using a path parameter and required query parameter.

    Parameters
    ----------
    item_id : str
        The unique identifier of the item (provided as a path parameter).

    needy : str
        A required query parameter that must be included in the request URL.

    skip : int, optional
        Number of items to skip for pagination. Default is 0.

    limit : int | None, optional
        Maximum number of items to return. If not provided, all items after
        the skip value will be returned.

    Returns
    -------
    dict
        A dictionary containing the item details along with pagination values.

    Example
    -------
    GET /items/123?needy=yes&skip=5&limit=10

"""

from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: int | None = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item
