from typing import Annotated

from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()


class CommonHeaders(BaseModel):
    """
    Pydantic model used to validate multiple headers.

    Note:
    convert_underscores=False means the header names must match
    exactly as written in this model (underscores will NOT be converted
    to hyphens automatically).
    """

    # Required headers
    host: str
    save_data: bool

    # Optional headers
    if_modified_since: str | None = None
    traceparent: str | None = None

    # Header that can appear multiple times
    x_tag: list[str] = []


@app.get("/items/")
async def read_items(
    headers: Annotated[CommonHeaders, Header(convert_underscores=False)],
):
    """
    Read request headers using a Pydantic model without converting
    underscores to hyphens.

    Required headers:
        host
        save_data

    Optional headers:
        if_modified_since
        traceparent
        x_tag (can appear multiple times)

    Returns
    -------
    dict
        Returns all validated header values.
    """

    return headers