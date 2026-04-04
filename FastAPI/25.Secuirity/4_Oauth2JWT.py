from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel

# ==============================
# 🔐 Security Configuration
# ==============================

"""
SECRET_KEY:
    Used to sign JWT tokens.
    Generate using: openssl rand -hex 32
"""
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

"""
ALGORITHM:
    Cryptographic algorithm used for JWT encoding/decoding.
"""
ALGORITHM = "HS256"

"""
ACCESS_TOKEN_EXPIRE_MINUTES:
    Token validity duration.
"""
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# ==============================
# 🗄️ Fake Database
# ==============================

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc",
        "disabled": False,
    }
}


# ==============================
# 📦 Pydantic Models
# ==============================

class Token(BaseModel):
    """
    Response model for authentication token.

    Attributes:
        access_token (str): JWT access token.
        token_type (str): Token type (usually 'bearer').
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Token payload data.

    Attributes:
        username (str | None): Extracted username (subject).
    """
    username: str | None = None


class User(BaseModel):
    """
    Public user model.

    Attributes:
        username (str): Unique username.
        email (str | None): Email address.
        full_name (str | None): Full name.
        disabled (bool | None): Account status.
    """
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    """
    Internal user model with hashed password.

    Extends:
        User
    """
    hashed_password: str


# ==============================
# 🔑 Password Hashing
# ==============================

password_hash = PasswordHash.recommended()

# Dummy hash to mitigate timing attacks
DUMMY_HASH = password_hash.hash("dummypassword")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password (str): User input password.
        hashed_password (str): Stored hashed password.

    Returns:
        bool: True if password matches, else False.
    """
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Generate a hashed password.

    Args:
        password (str): Plain password.

    Returns:
        str: Hashed password.
    """
    return password_hash.hash(password)


# ==============================
# 👤 User Management
# ==============================

def get_user(db: dict, username: str) -> UserInDB | None:
    """
    Retrieve a user from the database.

    Args:
        db (dict): Database.
        username (str): Username.

    Returns:
        UserInDB | None: User if exists, else None.
    """
    if username in db:
        return UserInDB(**db[username])
    return None


def authenticate_user(db: dict, username: str, password: str) -> UserInDB | bool:
    """
    Authenticate a user using username and password.

    Args:
        db (dict): Database.
        username (str): Username.
        password (str): Plain password.

    Returns:
        UserInDB | bool: User object if valid, else False.

    Security:
        Uses dummy hash to prevent timing attacks.
    """
    user = get_user(db, username)
    if not user:
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# ==============================
# 🎟️ JWT Token Handling
# ==============================

def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
) -> str:
    """
    Create a JWT access token.

    Args:
        data (dict): Payload data.
        expires_delta (timedelta | None): Expiry duration.

    Returns:
        str: Encoded JWT token.

    Notes:
        - Adds expiration (`exp`) claim.
        - Uses HS256 signing algorithm.
    """
    to_encode = data.copy()

    expire = (
        datetime.now(timezone.utc) + expires_delta
        if expires_delta
        else datetime.now(timezone.utc) + timedelta(minutes=15)
    )

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# OAuth2 scheme for extracting Bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> UserInDB:
    """
    Validate JWT token and retrieve current user.

    Args:
        token (str): Bearer token.

    Returns:
        UserInDB: Authenticated user.

    Raises:
        HTTPException (401): Invalid credentials.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)

    except InvalidTokenError:
        raise credentials_exception

    user = get_user(fake_users_db, username=token_data.username)

    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: Annotated[UserInDB, Depends(get_current_user)]
) -> UserInDB:
    """
    Ensure the authenticated user is active.

    Args:
        current_user (UserInDB): Authenticated user.

    Returns:
        UserInDB: Active user.

    Raises:
        HTTPException (400): If user is disabled.
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# ==============================
# 🚀 API Routes
# ==============================

app = FastAPI()


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    Authenticate user and generate JWT access token.

    Args:
        form_data (OAuth2PasswordRequestForm):
            Contains username and password.

    Returns:
        Token: JWT access token response.

    Raises:
        HTTPException (401): Invalid credentials.
    """
    user = authenticate_user(
        fake_users_db,
        form_data.username,
        form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> User:
    """
    Get current authenticated user's profile.

    Returns:
        User: Current user data.
    """
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    """
    Retrieve items owned by the current user.

    Returns:
        list: List of items.
    """
    return [{"item_id": "Foo", "owner": current_user.username}]