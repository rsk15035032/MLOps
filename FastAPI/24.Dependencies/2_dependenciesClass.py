from typing import Annotated, Optional, List, Dict

from fastapi import Depends, FastAPI

app = FastAPI()


# Simulated database
fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"},
]


class CommonQueryParams:
    """
    Dependency class for common query parameters.

    This class is used by FastAPI to automatically extract
    query parameters from incoming requests and provide them
    as an object.

    Attributes:
        q (Optional[str]): Search query string.
        skip (int): Number of items to skip (pagination offset).
        limit (int): Maximum number of items to return.
    """

    def __init__(
        self,
        q: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ):
        """
        Initialize query parameters.

        Args:
            q (Optional[str]): Search query.
            skip (int): Offset for pagination.
            limit (int): Limit for pagination.
        """
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/items/")
async def read_items(
    commons: Annotated[CommonQueryParams, Depends()]
) -> Dict[str, List[dict] | str]:
    """
    Retrieve items with optional filtering and pagination.

    Args:
        commons (CommonQueryParams): Injected query parameters.

    Returns:
        Dict: Response containing filtered items and optional query.
    """
    response: Dict = {}

    # Include search query in response if provided
    if commons.q:
        response["q"] = commons.q

    # Apply pagination using skip and limit
    items = fake_items_db[commons.skip : commons.skip + commons.limit]

    response["items"] = items

    return response