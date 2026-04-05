"""
FastAPI Dependency + BackgroundTasks Example (Production-Ready)

This module demonstrates:
- Dependency Injection with Depends
- Background task execution
- Logging query parameters asynchronously

Use cases:
- Request logging
- Audit trails
- Async side-effects (notifications, tracking, analytics)
"""

from pathlib import Path
import logging
from typing import Annotated

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException

# -------------------------------------------------------------------
# Logging Configuration
# -------------------------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------------------------------------------------
# FastAPI App Initialization
# -------------------------------------------------------------------

app = FastAPI(title="FAANG-Level Background + Dependency API")

# -------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------

LOG_FILE = Path("log.txt")


# -------------------------------------------------------------------
# Utility Functions
# -------------------------------------------------------------------

def write_log(message: str) -> None:
    """
    Write a log message to a file (executed in background).

    Args:
        message (str): Log message to write.

    Notes:
        - Uses append mode to prevent data loss.
        - Handles errors internally to avoid crashing background tasks.
    """
    try:
        with LOG_FILE.open(mode="a", encoding="utf-8") as log:
            log.write(message)

        logger.info(f"Log written: {message.strip()}")

    except Exception as e:
        logger.exception(f"Failed to write log: {e}")


# -------------------------------------------------------------------
# Dependency
# -------------------------------------------------------------------

def get_query(
    background_tasks: BackgroundTasks,
    q: str | None = None,
) -> str | None:
    """
    Dependency that processes query parameter `q`
    and logs it asynchronously if present.

    Args:
        background_tasks (BackgroundTasks): Task manager.
        q (str | None): Optional query parameter.

    Returns:
        str | None: The query value.
    """
    if q:
        message = f"found query: {q}\n"

        # Add background logging task
        background_tasks.add_task(write_log, message)

        logger.info(f"Query captured: {q}")

    return q


# -------------------------------------------------------------------
# API Endpoint
# -------------------------------------------------------------------

@app.post("/send-notification/{email}")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks,
    q: Annotated[str | None, Depends(get_query)],
):
    """
    Send a notification and log relevant data asynchronously.

    Args:
        email (str): Target email address.
        background_tasks (BackgroundTasks): Background task manager.
        q (str | None): Query parameter injected via dependency.

    Returns:
        dict: Response message.

    Raises:
        HTTPException: If email format is invalid.
    """
    # Basic validation (you can upgrade to Pydantic EmailStr)
    if "@" not in email:
        raise HTTPException(status_code=400, detail="Invalid email address")

    message = f"message to {email}\n"

    # Add background task
    background_tasks.add_task(write_log, message)

    return {
        "message": "Message scheduled",
        "email": email,
        "query": q,
    }