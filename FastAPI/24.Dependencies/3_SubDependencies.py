from typing import Annotated, Optional

from fastapi import Cookie, Depends, FastAPI

app = FastAPI()


def query_extractor(q: Optional[str] = None) -> Optional[str]:
    """
    Extract query parameter 'q' from the request.

    Args:
        q (Optional[str]): Query string parameter.

    Returns:
        Optional[str]: The query value if provided, else None.
    """
    return q


def query_or_cookie_extractor(
    q: Annotated[Optional[str], Depends(query_extractor)],
    last_query: Annotated[Optional[str], Cookie()] = None,
) -> Optional[str]:
    """
    Resolve query value using fallback logic.

    Priority:
    1. Use query parameter 'q' if provided
    2. Otherwise, use 'last_query' from cookies

    Args:
        q (Optional[str]): Extracted query parameter from dependency.
        last_query (Optional[str]): Cookie value storing last query.

    Returns:
        Optional[str]: Final resolved query value.
    """
    # If query param is missing, fallback to cookie
    if not q:
        return last_query
    return q


@app.get("/items/")
async def read_query(
    query_or_default: Annotated[
        Optional[str],
        Depends(query_or_cookie_extractor),
    ],
) -> dict:
    """
    Retrieve query value using dependency resolution.

    This endpoint demonstrates dependency chaining:
    - First extracts query param
    - Then falls back to cookie if needed

    Args:
        query_or_default (Optional[str]): Final resolved query value.

    Returns:
        dict: Response containing resolved query value.
    """
    return {"q_or_cookie": query_or_default}