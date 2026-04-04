from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

# Simulated database (in-memory)
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI()


def fake_hash_password(password: str) -> str:
    """
    Simulate password hashing.

    Args:
        password (str): Plain-text password.

    Returns:
        str: Fake hashed password.

    Notes:
        - This is NOT secure.
        - Replace with passlib/bcrypt in production.
    """
    return "fakehashed" + password


# OAuth2 scheme to extract Bearer token from Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    """
    Public user model (response schema).

    Attributes:
        username (str): Unique username.
        email (str | None): Email address.
        full_name (str | None): Full name of the user.
        disabled (bool | None): Account status.
    """
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    """
    Internal user model including sensitive data.

    Extends:
        User

    Attributes:
        hashed_password (str): Stored hashed password.
    """
    hashed_password: str


def get_user(db: dict, username: str) -> UserInDB | None:
    """
    Retrieve a user from the database.

    Args:
        db (dict): Database dictionary.
        username (str): Username to search.

    Returns:
        UserInDB | None: User object if found, else None.
    """
    if username in db:
        return UserInDB(**db[username])
    return None


def fake_decode_token(token: str) -> UserInDB | None:
    """
    Simulate decoding a token to retrieve user.

    Args:
        token (str): Access token.

    Returns:
        UserInDB | None: Corresponding user.

    Notes:
        - Token is treated as username (NOT secure).
        - Replace with JWT decoding in production.
    """
    return get_user(fake_users_db, token)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> UserInDB:
    """
    Dependency to get the current authenticated user.

    Args:
        token (str): Bearer token extracted from request.

    Returns:
        UserInDB: Authenticated user.

    Raises:
        HTTPException: If authentication fails (401 Unauthorized).
    """
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[UserInDB, Depends(get_current_user)]
) -> UserInDB:
    """
    Dependency to ensure the user is active.

    Args:
        current_user (UserInDB): Authenticated user.

    Returns:
        UserInDB: Active user.

    Raises:
        HTTPException: If user is disabled.
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """
    Authenticate user and return access token.

    Args:
        form_data (OAuth2PasswordRequestForm):
            Contains username and password from form data.

    Returns:
        dict: Access token and token type.

    Raises:
        HTTPException:
            - 400 if username or password is incorrect.

    Flow:
        1. Fetch user from DB
        2. Hash input password
        3. Compare with stored password
        4. Return token (username as token in this demo)

    Notes:
        - Uses OAuth2 password flow.
        - Replace with JWT token generation in production.
    """
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )

    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)

    if hashed_password != user.hashed_password:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
        )

    return {
        "access_token": user.username,
        "token_type": "bearer"
    }


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)]
):
    """
    Retrieve current authenticated and active user.

    Args:
        current_user (UserInDB): Active authenticated user.

    Returns:
        UserInDB: User details.

    Example:
        Request:
            GET /users/me
            Authorization: Bearer johndoe

        Response:
            {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "full_name": "John Doe",
                "disabled": false
            }
    """
    return current_user