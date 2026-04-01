from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/teleport")
async def get_teleport() -> RedirectResponse:
    """
    Redirect the user to another URL.

    This endpoint returns a RedirectResponse instead of JSON.
    When the user calls /teleport, the browser will automatically
    redirect to the provided URL.

    Returns
    -------
    RedirectResponse
        Redirects the user to the specified URL.
    """

    # Redirect the user to an external website
    return RedirectResponse(
        url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    )