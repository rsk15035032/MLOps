from typing import Annotated

from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()


class CommonHeaders(BaseModel):
    """
    Strict header validation model.

    model_config = {"extra": "forbid"} means:
    Only the headers defined below are allowed.
    If any extra header is sent → validation error.
    """

    model_config = {"extra": "forbid"}

    # Required headers
    host: str
    save_data: bool

    # Optional headers
    if_modified_since: str | None = None
    traceparent: str | None = None

    # Multiple header values allowed
    x_tag: list[str] = []


@app.get("/items/")
async def read_items(headers: Annotated[CommonHeaders, Header()]):
    """
    Read multiple request headers using a strict Pydantic model.

    Required headers:
        Host
        Save-Data

    Optional headers:
        If-Modified-Since
        Traceparent
        X-Tag (can appear multiple times)

    Extra headers:
        Not allowed (because extra="forbid")
    """

    return headers