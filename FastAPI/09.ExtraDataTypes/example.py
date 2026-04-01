from datetime import datetime, time, timedelta
from typing import Annotated
from uuid import UUID

from fastapi import Body, FastAPI

app = FastAPI()


@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Annotated[datetime, Body()],
    end_datetime: Annotated[datetime, Body()],
    process_after: Annotated[timedelta, Body()],
    repeat_at: Annotated[time | None, Body()] = None,
):
    """
    Calculate processing time and duration for a given item.

    Parameters
    ----------
    item_id : UUID
        Unique identifier of the item.

    start_datetime : datetime
        The date and time when the process is scheduled to start.

    end_datetime : datetime
        The date and time when the process is expected to end.

    process_after : timedelta
        Time delay after the start_datetime before the actual process begins.

    repeat_at : time | None, optional
        Specific time of the day when the process should repeat.
        If not provided, the process will not repeat.

    Returns
    -------
    dict
        A dictionary containing:
        - item_id
        - start_datetime
        - end_datetime
        - process_after
        - repeat_at
        - start_process (calculated start time after delay)
        - duration (total duration of the process)
    """

    # Calculate when the actual processing will start
    start_process = start_datetime + process_after

    # Calculate how long the process will run
    duration = end_datetime - start_process

    # Return all input values along with calculated values
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }