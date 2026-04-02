from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    """
    Custom handler for HTTP exceptions with logging.

    This handler intercepts all HTTPException errors raised in the application,
    logs the error details, and then delegates the response formatting back to
    FastAPI's default HTTP exception handler.

    Args:
        request: The incoming HTTP request.
        exc (StarletteHTTPException): The raised HTTP exception.

    Returns:
        Response: The default FastAPI HTTP exception response.

    Behavior:
        - Logs the exception for debugging/monitoring.
        - Reuses FastAPI's built-in handler to maintain standard response format.

    Example:
        If an endpoint raises:
            HTTPException(status_code=404, detail="Item not found")

        Console Output:
            OMG! An HTTP error!: HTTPException(...)

        Response:
            {
                "detail": "Item not found"
            }
    """

    # Log the exception (in production, use logging instead of print)
    print(f"OMG! An HTTP error!: {repr(exc)}")

    # Delegate response handling to FastAPI's default handler
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """
    Custom handler for request validation errors with logging.

    This handler captures validation errors caused by invalid client input
    (e.g., wrong data types, missing fields), logs the issue, and then
    delegates response generation to FastAPI's default validation handler.

    Args:
        request: The incoming HTTP request.
        exc (RequestValidationError): The validation error instance.

    Returns:
        Response: The default FastAPI validation error response.

    Behavior:
        - Logs validation issues for debugging/monitoring.
        - Uses FastAPI's default structured JSON error response.

    Example:
        Request:
            GET /items/abc

        Console Output:
            OMG! The client sent invalid data!: <validation error details>

        Response:
            {
                "detail": [
                    {
                        "loc": ["path", "item_id"],
                        "msg": "value is not a valid integer",
                        "type": "type_error.integer"
                    }
                ]
            }
    """

    # Log validation error (replace with proper logging in production)
    print(f"OMG! The client sent invalid data!: {exc}")

    # Delegate to FastAPI's default validation handler
    return await request_validation_exception_handler(request, exc)


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    """
    Retrieve an item by its ID.

    This endpoint expects an integer `item_id`. If invalid input is provided,
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
            GET /items/10

        Response:
            {
                "item_id": 10
            }

        Error Case 1 (Custom HTTPException):
            GET /items/3

            Response:
            {
                "detail": "Nope! I don't like 3."
            }

        Error Case 2 (Validation Error):
            GET /items/abc

            Response:
            {
                "detail": [
                    {
                        "loc": ["path", "item_id"],
                        "msg": "value is not a valid integer"
                    }
                ]
            }
    """

    # Raise custom HTTP exception for a specific value
    if item_id == 3:
        raise HTTPException(status_code=418, detail="Nope! I don't like 3.")

    # Return valid item_id
    return {"item_id": item_id}