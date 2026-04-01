from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class BaseUser(BaseModel):
    """
    Base model containing common user fields.

    This model is used as the response model to avoid
    returning sensitive data like passwords.
    """

    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(BaseUser):
    """
    Model used to receive user data from the request body.

    This model inherits from BaseUser and adds the password field.
    """

    password: str


@app.post("/user/")
async def create_user(user: UserIn) -> BaseUser:
    """
    Create a new user.

    The request body is validated using the UserIn model,
    but the response is automatically filtered using BaseUser.
    This prevents the password from being returned.

    Parameters
    ----------
    user : UserIn
        User data received in the request body (includes password)

    Returns
    -------
    BaseUser
        User data without the password
    """

    return user