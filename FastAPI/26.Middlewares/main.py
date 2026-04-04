import time

from fastapi import FastAPI, Request

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Middleware to measure request processing time.

    This middleware intercepts every incoming HTTP request,
    calculates how long it takes to process, and adds the
    duration to the response headers.

    Args:
        request (Request): Incoming HTTP request object.
        call_next (Callable): Function that forwards the request
                              to the next middleware or route handler.

    Returns:
        Response: HTTP response with added `X-Process-Time` header.

    Workflow:
        1. Capture start time before request processing
        2. Pass request to next handler (route or middleware)
        3. Capture end time after processing completes
        4. Calculate total processing time
        5. Attach it to response headers

    Header Added:
        X-Process-Time: Time taken (in seconds) to process request

    Notes:
        - Uses `time.perf_counter()` for high-precision timing
        - Useful for performance monitoring and debugging
        - In production, consider logging instead of exposing timing
          to avoid potential security insights

    Example:
        Response Headers:
            X-Process-Time: 0.00234
    """
    # Start high-resolution timer
    start_time = time.perf_counter()

    # Forward request to the next layer (route handler)
    response = await call_next(request)

    # Calculate total processing time
    process_time = time.perf_counter() - start_time

    # Add custom header to response
    response.headers["X-Process-Time"] = str(process_time)

    return response