from typing import Annotated
from fastapi import Header, HTTPException

# -------------------------------------------------------------------
# Dependency: Header Token Validation
# -------------------------------------------------------------------

async def get_token_header(x_token: Annotated[str, Header()]):
    """
    Validate the X-Token header.

    This dependency checks whether the incoming request contains
    a valid `X-Token` header. It is typically used for simple
    API key-based authentication.

    Args:
        x_token (str): Value of the 'X-Token' request header

    Raises:
        HTTPException: If the token is invalid

    Returns:
        None: If validation passes
    """
    if x_token != "fake-super-secret-token":
        raise HTTPException(
            status_code=400,
            detail="X-Token header invalid"
        )


# -------------------------------------------------------------------
# Dependency: Query Parameter Token Validation
# -------------------------------------------------------------------

async def get_query_token(token: str):
    """
    Validate token from query parameters.

    This dependency ensures that a specific query parameter `token`
    is present and matches an expected value.

    Args:
        token (str): Token provided as query parameter

    Raises:
        HTTPException: If the token is missing or incorrect

    Returns:
        None: If validation passes
    """
    if token != "jessica":
        raise HTTPException(
            status_code=400,
            detail="No Jessica token provided"
        )