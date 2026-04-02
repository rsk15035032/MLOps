from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserBase(BaseModel):
    """
    Base schema shared across multiple user models.

    Attributes:
        username (str): Unique username of the user.
        email (EmailStr): User's email address.
        full_name (str | None): Optional full name of the user.
    """
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(UserBase):
    """
    Schema for incoming user data (request body).

    Extends:
        UserBase

    Additional Attributes:
        password (str): Plain text password provided by the user.
    """
    password: str


class UserOut(UserBase):
    """
    Schema for outgoing user data (response).

    Extends:
        UserBase

    Note:
        Password is excluded for security reasons.
    """
    pass


class UserInDB(UserBase):
    """
    Internal schema representing how user data is stored in the database.

    Extends:
        UserBase

    Additional Attributes:
        hashed_password (str): Hashed version of the user's password.
    """
    hashed_password: str


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
    Simulates saving a user to a database.

    Steps:
        1. Hash the password.
        2. Convert UserIn -> UserInDB.
        3. Return stored user object.

    Args:
        user_in (UserIn): Incoming user data.

    Returns:
        UserInDB: Stored user representation.
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
        response_model=UserOut ensures sensitive data like password
        and hashed_password are NOT returned in the response.

    Args:
        user_in (UserIn): Incoming user data.

    Returns:
        UserOut: Safe user data without sensitive fields.
    """
    user_saved = fake_save_user(user_in)
    return user_saved