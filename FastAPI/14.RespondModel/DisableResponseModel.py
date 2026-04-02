from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/portal", response_model=None)
async def get_portal(teleport: bool = False) -> Response:
    """
    Return either a JSON response or a redirect response.

    If teleport=True → Redirect to external URL
    If teleport=False → Return JSON message
    """

    if teleport:
        return RedirectResponse(
            url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        )

    return {"message": "Here's your interdimensional portal."}