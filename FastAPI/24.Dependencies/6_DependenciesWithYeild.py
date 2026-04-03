from typing import Annotated, Generator

from fastapi import Depends, FastAPI, HTTPException, status

app = FastAPI()


class InternalError(Exception):
    """
    Custom exception representing an internal application error.
    """
    pass


def get_username() -> Generator[str, None, None]:
    """
    Dependency that provides a username.

    This uses `yield`, which allows:
    - Pre-processing before request (before yield)
    - Post-processing / cleanup (after yield)
    - Exception handling during request execution

    Yields:
        str: The username.
    """
    try:
        # Setup phase (before request handling)
        yield "Rick"

    except InternalError:
        # This block catches exceptions raised in the route
        print("InternalError caught in dependency, re-raising...")
        raise

    finally:
        # Cleanup logic (always runs)
        print("Cleanup logic executed (e.g., closing DB session)")


@app.get("/items/{item_id}")
def get_item(
    item_id: str,
    username: Annotated[str, Depends(get_username)],
) -> str:
    """
    Retrieve an item by ID.

    Demonstrates:
    - Dependency injection with `yield`
    - Exception propagation from route to dependency

    Args:
        item_id (str): ID of the requested item.
        username (str): Injected username from dependency.

    Returns:
        str: The item ID if valid.

    Raises:
        InternalError: If restricted item is accessed.
        HTTPException: If item is not found.
    """

    # Custom internal error (will be caught in dependency)
    if item_id == "portal-gun":
        raise InternalError(
            f"The portal gun is too dangerous to be owned by {username}"
        )

    # Standard API error
    if item_id != "plumbus":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found, there's only a plumbus here",
        )

    return item_id