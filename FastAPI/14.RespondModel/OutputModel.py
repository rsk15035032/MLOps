from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserIn(BaseModel):
    """
    Model used to receive user data from the request body.
    Contains sensitive data (password), so it should not
    be returned in the response.
    """

    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    """
    Model used for the response.

    This model excludes the password field to ensure
    sensitive data is not exposed.
    """

    username: str
    email: EmailStr
    full_name: str | None = None


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    """
    Create a new user.

    The request body is validated using UserIn.
    The response is filtered using UserOut, so the
    password will not be returned.

    Parameters
    ----------
    user : UserIn
        User data received in the request body.

    Returns
    -------
    UserOut
        User data without the password.
    """

    return user