from typing import Annotated

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(
    strange_header: Annotated[str | None, Header(convert_underscores=False)] = None,
):
    """
    Read a custom HTTP header without converting underscores to hyphens.

    By default, FastAPI converts underscores in header names into hyphens.
    Example:
        strange_header  ->  strange-header

    But in this endpoint, convert_underscores=False is used,
    so the header name must be sent exactly as: strange_header

    Parameters
    ----------
    strange_header : str | None, optional
        Value of the custom header named 'strange_header'.
        If the header is not provided, the value will be None.

    Returns
    -------
    dict
        A dictionary containing the received header value.
    """

    # Return the value of the header received in the request
    return {"strange_header": strange_header}