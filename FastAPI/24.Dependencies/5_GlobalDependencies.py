from typing import Annotated, List, Dict

from fastapi import Depends, FastAPI, Header, HTTPException, status

# Constants for secrets (avoid hardcoding in functions)
SECRET_TOKEN = "fake-super-secret-token"
SECRET_KEY = "fake-super-secret-key"


async def verify_token(x_token: Annotated[str, Header()]) -> None:
    """
    Validate the X-Token header.

    This dependency ensures that every request contains a valid token.
    Applied globally to all routes via FastAPI app.

    Args:
        x_token (str): Token from request header.

    Raises:
        HTTPException: If token is invalid.
    """
    if x_token != SECRET_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid X-Token",
        )


async def verify_key(x_key: Annotated[str, Header()]) -> str:
    """
    Validate the X-Key header.

    Args:
        x_key (str): API key from request header.

    Returns:
        str: Validated API key.

    Raises:
        HTTPException: If key is invalid.
    """
    if x_key != SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid X-Key",
        )
    return x_key


# Apply dependencies globally to ALL routes
app = FastAPI(
    dependencies=[
        Depends(verify_token),
        Depends(verify_key),
    ]
)


@app.get("/items/")
async def read_items() -> List[Dict[str, str]]:
    """
    Retrieve list of items.

    This endpoint is protected by global dependencies:
    - Requires valid X-Token
    - Requires valid X-Key

    Returns:
        List[Dict[str, str]]: List of items.
    """
    return [{"item": "Portal Gun"}, {"item": "Plumbus"}]


@app.get("/users/")
async def read_users() -> List[Dict[str, str]]:
    """
    Retrieve list of users.

    Protected by the same global dependencies.

    Returns:
        List[Dict[str, str]]: List of users.
    """
    return [{"username": "Rick"}, {"username": "Morty"}]