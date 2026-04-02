from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class UnicornException(Exception):
    """
    Custom exception class for handling unicorn-related errors.

    This exception is raised when a specific condition related to a unicorn
    occurs (e.g., a forbidden or unexpected unicorn name).

    Attributes:
        name (str): The name of the unicorn that caused the exception.
    """

    def __init__(self, name: str):
        self.name = name


app = FastAPI()


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    """
    Handle UnicornException globally.

    This custom exception handler intercepts all UnicornException errors
    raised within the application and returns a structured JSON response
    with a custom HTTP status code.

    Args:
        request (Request): The incoming HTTP request object.
        exc (UnicornException): The raised exception instance.

    Returns:
        JSONResponse: A JSON response containing the error message.

    Example Response:
        Status Code: 418
        {
            "message": "Oops! yolo did something. There goes a rainbow..."
        }
    """

    # Return a custom JSON response with status code 418 (I'm a teapot)
    return JSONResponse(
        status_code=418,
        content={
            "message": f"Oops! {exc.name} did something. There goes a rainbow..."
        },
    )


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    """
    Retrieve a unicorn by name.

    This endpoint returns the unicorn name unless it matches a specific
    restricted value ("yolo"), in which case a UnicornException is raised.

    Args:
        name (str): The name of the unicorn.

    Returns:
        dict: A dictionary containing the unicorn name.

    Raises:
        UnicornException: If the unicorn name is "yolo".

    Example:
        Request:
            GET /unicorns/sparkle

        Response:
            {
                "unicorn_name": "sparkle"
            }

        Error Case:
            GET /unicorns/yolo

            Status Code: 418
            {
                "message": "Oops! yolo did something. There goes a rainbow..."
            }
    """

    # Raise custom exception for a specific name
    if name == "yolo":
        raise UnicornException(name=name)

    # Return unicorn name if valid
    return {"unicorn_name": name}