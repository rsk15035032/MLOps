from fastapi import FastAPI

app = FastAPI()




@app.get("/users")
async def read_users():

    """
    Retrieve a list of users.

    This endpoint returns a simple list of user names.
    It is used to demonstrate how a basic GET endpoint
    works in FastAPI.

    Returns:
        list: A list of user names.

    Example:
        GET /users

        Response:
        [
            "Rick",
            "Morty"
        ]
    """
    return ["Rick", "Morty"]


@app.get("/users")
async def read_users2():
    
    
    """
    Duplicate endpoint for the same route.

    This function is mapped to the same path (/users) and
    HTTP method (GET) as the previous endpoint. In FastAPI,
    the second function will override the first one, so only
    this response will be returned.

    Returns:
        list: A list of user names.

    Example:
        GET /users

        Response:
        [
            "Bean",
            "Elfo"
        ]
    """
    return ["Bean", "Elfo"]