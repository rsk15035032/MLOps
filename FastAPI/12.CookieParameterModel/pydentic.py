from typing import Annotated

from fastapi import Cookie, FastAPI
from pydantic import BaseModel

app = FastAPI()


class Cookies(BaseModel):
    """
    Pydantic model used to validate multiple cookies.

    session_id         -> required cookie
    fatebook_tracker   -> optional cookie
    googall_tracker    -> optional cookie
    """

    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None


@app.get("/items/")
async def read_items(cookies: Annotated[Cookies, Cookie()]):
    """
    Read multiple cookies using a Pydantic model.

    Instead of reading each cookie separately, FastAPI maps all cookies
    to the Cookies model and validates them automatically.

    Required Cookie:
        session_id

    Optional Cookies:
        fatebook_tracker
        googall_tracker

    Returns
    -------
    Cookies
        Returns all cookie values as a validated Pydantic model.
    """

    # Return validated cookies
    return cookies