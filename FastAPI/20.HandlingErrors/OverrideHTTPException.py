from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    """
    Handle all HTTP exceptions raised by Starlette/FastAPI.

    This global exception handler intercepts HTTPException instances
    and returns a plain text response instead of the default JSON format.

    Args:
        request: The incoming HTTP request.
        exc (StarletteHTTPException): The raised HTTP exception.

    Returns:
        PlainTextResponse: A plain text response containing the error detail.

    Example:
        If an endpoint raises:
            HTTPException(status_code=404, detail="Item not found")

        Response:
            Status Code: 404
            Body: Item not found
    """

    # Convert exception detail into plain text response
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    """
    Handle request validation errors globally.

    This handler captures validation errors triggered by invalid request data
    (e.g., wrong data types, missing fields) and formats them into a readable
    plain text response.

    Args:
        request: The incoming HTTP request.
        exc (RequestValidationError): The validation error object.

    Returns:
        PlainTextResponse: A formatted plain text response listing validation errors.

    Example:
        Request:
            GET /items/abc

        Response:
            Status Code: 400
            Body:
                Validation errors:
                Field: ('path', 'item_id'), Error: value is not a valid integer
    """

    # Initialize error message
    message = "Validation errors:"

    # Loop through all validation errors and append details
    for error in exc.errors():
        message += f"\nField: {error['loc']}, Error: {error['msg']}"

    # Return formatted validation error response
    return PlainTextResponse(message, status_code=400)


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    """
    Retrieve an item by its ID.

    This endpoint expects an integer `item_id`. If the value is invalid,
    the RequestValidationError handler will be triggered automatically.
    Additionally, a custom HTTPException is raised for a specific value.

    Args:
        item_id (int): The ID of the item.

    Returns:
        dict: A dictionary containing the item ID.

    Raises:
        HTTPException:
            - 418 I'm a teapot: If item_id equals 3.

    Example:
        Request:
            GET /items/5

        Response:
            {
                "item_id": 5
            }

        Error Case 1 (Custom Exception):
            GET /items/3

            Status Code: 418
            Body:
                Nope! I don't like 3.

        Error Case 2 (Validation Error):
            GET /items/abc

            Status Code: 400
            Body:
                Validation errors:
                Field: ('path', 'item_id'), Error: value is not a valid integer
    """

    # Raise custom HTTP exception for a specific value
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")

    # Return valid item_id
    return {"item_id": item_id}