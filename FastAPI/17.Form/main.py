from typing import Annotated

from fastapi import FastAPI, Form

app = FastAPI()


@app.post("/login/")
async def login(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    """
    Handle user login using form data.

    Args:
        username (str): Username submitted via form data.
        password (str): Password submitted via form data.

    Returns:
        dict: Contains the submitted username.

    Note:
        - `Form()` tells FastAPI to expect data as form-encoded (application/x-www-form-urlencoded)
        - Commonly used with HTML forms or login endpoints
        - Password is not returned for security reasons
    """
    return {"username": username}  # Echo back username (for demo purposes)