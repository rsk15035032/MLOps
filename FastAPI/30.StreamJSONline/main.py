from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json
import asyncio

app = FastAPI()


# -------------------------------------------------------------------
# Data Model
# -------------------------------------------------------------------

class Item(BaseModel):
    """
    Represents an item entity.

    Attributes:
        name (str): Name of the item
        description (Optional[str]): Description of the item
    """
    name: str
    description: str | None = None


# -------------------------------------------------------------------
# In-Memory Data Source
# -------------------------------------------------------------------

items = [
    Item(name="Plumbus", description="A multi-purpose household device."),
    Item(name="Portal Gun", description="A portal opening device."),
    Item(name="Meeseeks Box", description="A box that summons a Meeseeks."),
]


# -------------------------------------------------------------------
# Streaming Endpoint (Production-Ready)
# -------------------------------------------------------------------

@app.get("/items/stream")
async def stream_items():
    """
    Stream items using JSON Lines (NDJSON).

    This endpoint sends data incrementally instead of returning
    the full response at once.

    Use cases:
        - Large datasets
        - Real-time APIs
        - ML/LLM streaming responses

    Returns:
        StreamingResponse: Stream of JSON objects (one per line)
    """

    async def event_generator():
        """
        Async generator that yields items one by one.

        Yields:
            str: JSON serialized item followed by newline
        """
        for item in items:
            # Simulate delay (useful for real-time streaming demo)
            await asyncio.sleep(0.5)

            # Convert item to JSON string (NDJSON format)
            yield json.dumps(item.model_dump()) + "\n"

    return StreamingResponse(
        event_generator(),
        media_type="application/x-ndjson"  # Standard for streaming JSON
    )


# -------------------------------------------------------------------
# Health Check / Root Endpoint
# -------------------------------------------------------------------

@app.get("/")
async def root():
    """
    Root endpoint for health check.

    Returns:
        dict: Simple welcome message
    """
    return {"message": "Streaming API is running 🚀"}