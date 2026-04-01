from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/portal", response_model=None)
async def get_portal(teleport: bool = False) -> Response:
    """
    Return either a JSON response or a redirect response based on a query parameter.

    If teleport = True:
        The user is redirected to another URL.

    If teleport = False:
        A normal JSON response is returned.

    Parameters
    ----------
    teleport : bool, optional
        Query parameter that decides whether the response should redirect
        the user to another page.

    Returns
    -------
    Response
        RedirectResponse when teleport=True
        JSON response when teleport=False
    """

    # If teleport is True, redirect the user
    if teleport:
        return RedirectResponse(
            url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        )

    # Otherwise return a normal JSON response
    return {"message": "Here's your interdimensional portal."}