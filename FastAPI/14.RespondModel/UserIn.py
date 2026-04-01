from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserIn(BaseModel):
    """
    Model used to receive user data from the request body.

    WARNING:
    This model contains a password field, so it should NOT be
    returned directly in the response in a real production app.
    """

    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


# Don't do this in production!
@app.post("/user/")
async def create_user(user: UserIn) -> UserIn:
    """
    Create a new user.

    This endpoint receives user data including the password.
    It returns the same user object, which means the password
    will also be returned in the response.

    This is only for learning/demo purposes and should NOT
    be done in a real-world application.

    Parameters
    ----------
    user : UserIn
        User data received in the request body.

    Returns
    -------
    UserIn
        The same user object (including password).
    """

    return user