from typing import Annotated, List, Dict

from fastapi import Depends, FastAPI, Header, HTTPException, status

app = FastAPI()


async def verify_token(x_token: Annotated[str, Header()]) -> None:
    """
    Validate the X-Token header.

    This dependency ensures that every request includes a valid token.
    It does not return anything; it only raises an exception if invalid.

    Args:
        x_token (str): Token provided in request header.

    Raises:
        HTTPException: If token is invalid.
    """
    if x_token != "fake-super-secret-token":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="X-Token header invalid",
        )


async def verify_key(x_key: Annotated[str, Header()]) -> str:
    """
    Validate the X-Key header.

    Args:
        x_key (str): Key provided in request header.

    Returns:
        str: The validated key (can be used in downstream logic).

    Raises:
        HTTPException: If key is invalid.
    """
    if x_key != "fake-super-secret-key":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="X-Key header invalid",
        )
    return x_key


@app.get(
    "/items/",
    dependencies=[Depends(verify_token), Depends(verify_key)],
)
async def read_items() -> List[Dict[str, str]]:
    """
    Retrieve list of items.

    This endpoint is protected by header-based dependencies:
    - Requires valid X-Token
    - Requires valid X-Key

    Returns:
        List[Dict[str, str]]: List of items.
    """
    return [{"item": "Foo"}, {"item": "Bar"}]