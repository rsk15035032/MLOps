from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

# OAuth2 scheme to extract Bearer token from Authorization header
# tokenUrl specifies the endpoint where clients obtain the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    """
    Pydantic model representing a user.

    Attributes:
        username (str): Unique identifier for the user.
        email (str | None): User's email address.
        full_name (str | None): Full name of the user.
        disabled (bool | None): Indicates if the user account is inactive.
    """
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


def fake_decode_token(token: str) -> User:
    """
    Simulate decoding of an access token.

    Args:
        token (str): The raw JWT or access token.

    Returns:
        User: A mock user object derived from the token.

    Notes:
        - This is NOT secure and only for demonstration purposes.
        - In production, replace this with:
            - JWT decoding (e.g., using PyJWT)
            - Signature verification
            - Expiry validation
            - Database lookup
    """
    return User(
        username=token + "fakedecoded",
        email="john@example.com",
        full_name="John Doe"
    )


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    """
    Dependency to retrieve the current authenticated user.

    Args:
        token (str): Bearer token extracted via OAuth2PasswordBearer.

    Returns:
        User: The authenticated user object.

    Workflow:
        1. Extract token from Authorization header
        2. Decode token
        3. Return user object

    Raises:
        (In real implementation)
        - HTTPException(401): Invalid or expired token
    """
    user = fake_decode_token(token)
    return user


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    """
    Retrieve details of the currently authenticated user.

    Args:
        current_user (User): Injected user from authentication dependency.

    Returns:
        User: The current user's information.

    Example:
        Request:
            GET /users/me
            Authorization: Bearer mytoken

        Response:
            {
                "username": "mytokenfakedecoded",
                "email": "john@example.com",
                "full_name": "John Doe",
                "disabled": null
            }
    """
    return current_user