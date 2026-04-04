from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

# OAuth2 scheme instance
# This defines how the token will be extracted from the request (Authorization header)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
async def read_items(
    token: Annotated[str, Depends(oauth2_scheme)]
):
    """
    Retrieve items using OAuth2 authentication.

    This endpoint demonstrates how to use FastAPI's built-in
    OAuth2PasswordBearer dependency to extract a Bearer token
    from the Authorization header.

    Args:
        token (str): Access token extracted from the request using OAuth2 scheme.

    Returns:
        dict: A dictionary containing the provided access token.

    Notes:
        - The token is expected in the format:
          Authorization: Bearer <token>
        - `tokenUrl="token"` indicates where the client should request the token.
        - This example does NOT validate the token (no decoding or verification).
        - In production, you should:
            - Validate JWT tokens
            - Check expiration
            - Verify user permissions/scopes

    Example:
        Request:
            GET /items/
            Headers:
                Authorization: Bearer mysecrettoken

        Response:
            {
                "token": "mysecrettoken"
            }
    """
    return {"token": token}