from typing import Annotated

from fastapi import Cookie, FastAPI

app = FastAPI()


@app.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    """
    Read a cookie value from the request.

    This endpoint retrieves a cookie named `ads_id` from the client request.
    If the cookie is present, its value is returned.
    If the cookie is not present, the endpoint returns None.

    Parameters
    ----------
    ads_id : str | None, optional
        Value of the cookie named 'ads_id'.
        If the cookie does not exist, the value will be None.

    Returns
    -------
    dict
        A dictionary containing the cookie value.
        Example:
        {
            "ads_id": "abc123"
        }
    """

    # Return the value received from the cookie
    return {"ads_id": ads_id}