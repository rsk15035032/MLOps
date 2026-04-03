from typing import Annotated, Optional, Dict

from fastapi import Depends, FastAPI

app = FastAPI()


async def common_parameters(
    q: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
) -> Dict[str, Optional[int | str]]:
    """
    Common query parameters dependency.

    This function extracts and returns reusable query parameters
    that can be shared across multiple endpoints.

    Args:
        q (Optional[str]): Search query string.
        skip (int): Number of records to skip (pagination offset).
        limit (int): Maximum number of records to return.

    Returns:
        Dict[str, Optional[int | str]]: Dictionary containing query parameters.
    """
    return {"q": q, "skip": skip, "limit": limit}


# Create a reusable dependency alias using Annotated
CommonsDep = Annotated[Dict[str, Optional[int | str]], Depends(common_parameters)]


@app.get("/items/")
async def read_items(commons: CommonsDep) -> Dict[str, Optional[int | str]]:
    """
    Retrieve items with shared query parameters.

    Args:
        commons (dict): Injected query parameters from dependency.

    Returns:
        dict: The query parameters used for fetching items.
    """
    return commons


@app.get("/users/")
async def read_users(commons: CommonsDep) -> Dict[str, Optional[int | str]]:
    """
    Retrieve users with shared query parameters.

    Args:
        commons (dict): Injected query parameters from dependency.

    Returns:
        dict: The query parameters used for fetching users.
    """
    return commons