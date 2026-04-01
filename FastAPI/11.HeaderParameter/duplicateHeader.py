from typing import Annotated

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(x_token: Annotated[list[str] | None, Header()] = None):
    """
    Read multiple values of the same HTTP header.

    This endpoint accepts multiple headers with the same name (X-Token).
    FastAPI automatically collects all header values into a list.

    Example:
        X-Token: token1
        X-Token: token2

    Parameters
    ----------
    x_token : list[str] | None, optional
        A list containing all values passed in the X-Token header.
        If no header is provided, the value will be None.

    Returns
    -------
    dict
        A dictionary containing all received X-Token values.
    """

    # Return all received header values
    return {"X-Token values": x_token}