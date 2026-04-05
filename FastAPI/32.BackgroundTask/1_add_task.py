"""
FastAPI Background Tasks Example (Production-Ready)

This module demonstrates how to execute non-blocking background tasks
using FastAPI's BackgroundTasks utility.

Use cases:
- Sending emails
- Writing logs
- Triggering async pipelines
- ML inference post-processing
"""

from pathlib import Path
import logging

from fastapi import BackgroundTasks, FastAPI, HTTPException

# -------------------------------------------------------------------
# Logging Configuration
# -------------------------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------------------------------------------------
# FastAPI App Initialization
# -------------------------------------------------------------------

app = FastAPI(title="Background Tasks API")

# -------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------

LOG_FILE = Path("log.txt")


# -------------------------------------------------------------------
# Background Task Function
# -------------------------------------------------------------------

def write_notification(email: str, message: str = "") -> None:
    """
    Write a notification message to a log file.

    This function runs in the background after the API response is returned.

    Args:
        email (str): Recipient email.
        message (str, optional): Notification message.

    Raises:
        Exception: Logs any exception internally (does not crash API).
    """
    try:
        content = f"notification for {email}: {message}\n"

        # ✅ Use append mode instead of write (avoids overwriting file)
        with LOG_FILE.open(mode="a", encoding="utf-8") as file:
            file.write(content)

        logger.info(f"Notification written for {email}")

    except Exception as e:
        # ❗ Background tasks should never crash silently
        logger.exception(f"Failed to write notification: {e}")


# -------------------------------------------------------------------
# API Endpoint
# -------------------------------------------------------------------

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    """
    Trigger a background notification task.

    Args:
        email (str): Target email address.
        background_tasks (BackgroundTasks): FastAPI background task manager.

    Returns:
        dict: Confirmation message.

    Notes:
        - Task runs AFTER response is sent.
        - Non-blocking → improves API latency.
    """
    if "@" not in email:
        raise HTTPException(status_code=400, detail="Invalid email address")

    background_tasks.add_task(
        write_notification,
        email,
        message="some notification",
    )

    return {
        "message": "Notification scheduled in the background",
        "email": email,
    }