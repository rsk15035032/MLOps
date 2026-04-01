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
    Process an item using datetime and time-based parameters.

    This endpoint receives different time-related inputs such as
    start time, end time, delay before processing, and an optional
    repeat time. It then calculates when the actual processing starts
    and how long the processing lasts.

    Parameters
    ----------
    item_id : UUID
        Unique identifier of the item passed in the path parameter.

    start_datetime : datetime
        The datetime when the process is scheduled to start.

    end_datetime : datetime
        The datetime when the process is expected to finish.

    process_after : timedelta
        The delay after start_datetime before the actual processing begins.

    repeat_at : time | None, optional
        Specific time of day when the process should repeat.
        If not provided, the process will run only once.

    Returns
    -------
    dict
        A dictionary containing the original input values along with:
        - start_process : datetime
            The calculated start time after adding the delay.
        - duration : timedelta
            Total duration from start_process to end_datetime.
    """

    # Calculate the actual processing start time
    start_process = start_datetime + process_after

    # Calculate the total duration of the processing
    duration = end_datetime - start_process

    # Return both input values and calculated results
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }