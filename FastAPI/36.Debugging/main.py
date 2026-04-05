"""
FastAPI Application Entry Point

This module defines a simple FastAPI application and demonstrates:
- Basic route handling
- Uvicorn server execution
- Proper entry-point pattern

Use cases:
- API services
- ML model serving endpoints
- Microservice entry point
"""

import os
import uvicorn
from fastapi import FastAPI

# -------------------------------------------------------------------
# App Initialization
# -------------------------------------------------------------------

app = FastAPI(
    title="FastAPI App",
    description="Simple API with production-ready structure.",
    version="1.0.0",
)

# -------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------

@app.get("/", summary="Health check endpoint")
def root() -> dict[str, str]:
    """
    Root endpoint for health check.

    Returns:
        dict[str, str]: Simple greeting response.
    """
    a = "a"
    b = f"b{a}"  # cleaner than "b" + a
    return {"message": f"hello world {b}"}


# -------------------------------------------------------------------
# Entry Point
# -------------------------------------------------------------------

if __name__ == "__main__":
    """
    Run the application using Uvicorn.

    Notes:
        - Used for local development only.
        - In production, use CLI: `uvicorn main:app`
    """
    uvicorn.run(
        "main:app",  # string reference (better for reload & workers)
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=True,  # auto-reload in development
        log_level="info",
    )