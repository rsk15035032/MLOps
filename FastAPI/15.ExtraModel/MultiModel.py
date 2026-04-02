from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserIn(BaseModel):
    """
    Schema for incoming user data (request body).

    Attributes:
        username (str): Unique username of the user.
        password (str): Plain text password provided by the user.
        email (EmailStr): User's email address (validated).
        full_name (str | None): Optional full name of the user.
    """
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOut(BaseModel):
    """
    Schema for outgoing user data (response).

    Note:
        Password is intentionally excluded for security reasons.
    """
    username: str
    email: EmailStr
    full_name: str | None = None


class UserInDB(BaseModel):
    """
    Internal schema representing how user data is stored in the database.

    Attributes:
        username (str): Username of the user.
        hashed_password (str): Hashed version of the password.
        email (EmailStr): User's email address.
        full_name (str | None): Optional full name.
    """
    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None


def fake_password_hasher(raw_password: str):
    """
    Simulates password hashing.

    Args:
        raw_password (str): Plain text password.

    Returns:
        str: Fake hashed password.
    """
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    """
    Simulates saving a user to the database.

    Steps:
        1. Hash the incoming password.
        2. Convert UserIn -> UserInDB.
        3. Return stored user object.

    Args:
        user_in (UserIn): Incoming user data.

    Returns:
        UserInDB: User object as stored in the database.
    """
    hashed_password = fake_password_hasher(user_in.password)

    # Convert input model to dict and add hashed_password
    user_in_db = UserInDB(
        **user_in.model_dump(),
        hashed_password=hashed_password
    )

    print("User saved! ..not really")  # Mock persistence
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    """
    Create a new user.

    Workflow:
        - Accepts user input (UserIn)
        - Saves user (simulated)
        - Returns safe response (UserOut)

    Important:
        response_model=UserOut ensures that the password
        is never exposed in the API response.

    Args:
        user_in (UserIn): Incoming user data.

    Returns:
        UserOut: Safe user data without password.
    """
    user_saved = fake_save_user(user_in)
    return user_saved