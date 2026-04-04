from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header
from .internal import admin
from .routers import items, users

# -------------------------------------------------------------------
# Application Initialization
# -------------------------------------------------------------------

app = FastAPI(
    dependencies=[Depends(get_query_token)]  # Global dependency (applies to all routes)
)


# -------------------------------------------------------------------
# Router Registration
# -------------------------------------------------------------------

# Public user-related routes
app.include_router(users.router)

# Item-related routes (already protected internally via router dependency)
app.include_router(items.router)

# Admin routes with additional security layer
app.include_router(
    admin.router,
    prefix="/admin",  # All admin routes will start with /admin
    tags=["admin"],   # Group in API docs
    dependencies=[Depends(get_token_header)],  # Extra security for admin endpoints
    responses={418: {"description": "I'm a teapot"}},  # Custom response example
)


# -------------------------------------------------------------------
# Root Endpoint
# -------------------------------------------------------------------

@app.get("/")
async def root():
    """
    Root endpoint of the application.

    This endpoint serves as a basic health check or welcome message.

    Note:
        Global dependency `get_query_token` is applied,
        so a valid query token is required to access this route.

    Returns:
        dict: Welcome message
    """
    return {"message": "Hello Bigger Applications!"}