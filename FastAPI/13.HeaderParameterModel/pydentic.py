from typing import Annotated

from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()


class CommonHeaders(BaseModel):
    """
    Pydantic model used to validate multiple HTTP headers at once.
    """

    # Required header
    host: str

    # Required header (converted from: Save-Data)
    save_data: bool

    # Optional headers
    if_modified_since: str | None = None
    traceparent: str | None = None

    # Multiple header values allowed
    x_tag: list[str] = []


@app.get("/items/")
async def read_items(headers: Annotated[CommonHeaders, Header()]):
    """
    Read and validate multiple request headers using a Pydantic model.

    FastAPI automatically:
    - converts header names (save-data → save_data)
    - validates the values using the Pydantic model
    - supports multiple values for the same header (like X-Tag)

    Returns
    -------
    CommonHeaders
        Returns all validated header values.
    """

    return headers