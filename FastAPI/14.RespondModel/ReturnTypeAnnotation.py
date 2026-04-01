from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, RedirectResponse

app = FastAPI()


@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response:
    """
    Return different responses based on a query parameter.

    If teleport = True:
        Redirects the user to another URL.

    If teleport = False:
        Returns a normal JSON response.

    Parameters
    ----------
    teleport : bool, optional
        Query parameter that decides whether to redirect the user.

    Returns
    -------
    Response
        RedirectResponse if teleport=True
        JSONResponse if teleport=False
    """

    # If teleport is True, redirect the user
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    # Otherwise return a normal JSON response
    return JSONResponse(
        content={"message": "Here's your interdimensional portal."}
    )