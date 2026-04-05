"""
Production-Grade FastAPI SSE (Server-Sent Events) Streaming

Features:
- Async streaming (non-blocking)
- Proper SSE event formatting
- Client disconnect handling
- Structured logging
- Type safety with Pydantic
- Extensible for ML/LLM streaming pipelines
"""

from __future__ import annotations

import asyncio
import json
import logging
from collections.abc import AsyncGenerator
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# -------------------------------------------------------------------
# Logging Configuration
# -------------------------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------------------------------------------------
# FastAPI App Initialization
# -------------------------------------------------------------------

app = FastAPI(title="SSE Streaming API")


# -------------------------------------------------------------------
# Data Model
# -------------------------------------------------------------------

class Item(BaseModel):
    """
    Represents a streamable item entity.

    Attributes:
        name (str): Name of the item.
        description (str | None): Optional description.
    """
    name: str
    description: str | None = None


# -------------------------------------------------------------------
# Mock Data Source (Replace with DB / Kafka / ML Model)
# -------------------------------------------------------------------

ITEMS: list[Item] = [
    Item(name="Plumbus", description="A multi-purpose household device."),
    Item(name="Portal Gun", description="A portal opening device."),
    Item(name="Meeseeks Box", description="Summons a Meeseeks."),
]


# -------------------------------------------------------------------
# SSE Utility
# -------------------------------------------------------------------

def format_sse(
    data: Any,
    event: str | None = None,
    event_id: int | None = None,
) -> str:
    """
    Format data into SSE-compliant string.

    Args:
        data (Any): Payload to send to client.
        event (str, optional): Event type.
        event_id (int, optional): Unique event ID.

    Returns:
        str: Properly formatted SSE message.
    """
    message = ""

    if event_id is not None:
        message += f"id: {event_id}\n"

    if event:
        message += f"event: {event}\n"

    # Ensure JSON serialization
    payload = json.dumps(data, default=str)
    message += f"data: {payload}\n\n"

    return message


# -------------------------------------------------------------------
# Streaming Generator
# -------------------------------------------------------------------

async def item_event_generator(request: Request) -> AsyncGenerator[str, None]:
    """
    Async generator for streaming items as SSE events.

    Handles:
    - Client disconnects
    - Controlled streaming delay
    - Error propagation

    Args:
        request (Request): FastAPI request object.

    Yields:
        str: SSE formatted event.
    """
    try:
        for idx, item in enumerate(ITEMS):
            # Handle client disconnect (important for production)
            if await request.is_disconnected():
                logger.info("Client disconnected. Stopping stream.")
                break

            # Simulate real-time streaming delay
            await asyncio.sleep(1)

            logger.info(f"Streaming item {idx}: {item.name}")

            yield format_sse(
                data=item.model_dump(),
                event="item",
                event_id=idx,
            )

        # Send completion event
        yield format_sse(data={"status": "completed"}, event="end")

    except Exception as e:
        logger.exception("Error during streaming")

        # Send error event to client
        yield format_sse(
            data={"error": str(e)},
            event="error",
        )


# -------------------------------------------------------------------
# API Endpoint
# -------------------------------------------------------------------

@app.get("/items/stream")
async def stream_items(request: Request) -> StreamingResponse:
    """
    Stream items using Server-Sent Events (SSE).

    Args:
        request (Request): Incoming request object.

    Returns:
        StreamingResponse: SSE stream response.

    Response:
        - event: item → each item
        - event: end → stream completed
        - event: error → error occurred

    Example (JS client):
        const evtSource = new EventSource("/items/stream");
        evtSource.onmessage = (event) => console.log(event.data);
    """
    return StreamingResponse(
        item_event_generator(request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable buffering (NGINX)
        },
    )