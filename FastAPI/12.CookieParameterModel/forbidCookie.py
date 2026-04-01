from typing import Annotated

from fastapi import Cookie, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Cookies(BaseModel):
    """
    Pydantic model used to validate cookies strictly.

    model_config = {"extra": "forbid"} means:
    - Only the cookies defined in this model are allowed
    - If any extra cookie is sent, FastAPI will raise a validation error
    """

    model_config = {"extra": "forbid"}

    # Required cookie
    session_id: str

    # Optional cookies
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None


@app.get("/items/")
async def read_items(cookies: Annotated[Cookies, Cookie()]):
    """
    Read cookies using a strict Pydantic model.

    Required cookie:
        session_id

    Optional cookies:
        fatebook_tracker
        googall_tracker

    Extra cookies:
        Not allowed (because extra="forbid")

    Returns
    -------
    Cookies
        Returns validated cookie values.
    """

    # Return validated cookies
    return cookies