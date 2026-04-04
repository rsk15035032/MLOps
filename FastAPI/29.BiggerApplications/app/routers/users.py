from fastapi import APIRouter

# Create a router instance to group related endpoints
router = APIRouter()


@router.get("/users/", tags=["users"])
async def read_users():
    """
    Retrieve a list of users.

    This endpoint returns a static list of users.
    Typically, this would fetch data from a database.

    Returns:
        list[dict]: A list of user objects containing usernames
    """
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/users/me", tags=["users"])
async def read_user_me():
    """
    Retrieve the current authenticated user.

    In a real-world application, this endpoint would:
    - Extract user info from authentication (JWT/OAuth2)
    - Return the currently logged-in user

    Returns:
        dict: Current user information
    """
    return {"username": "fakecurrentuser"}


@router.get("/users/{username}", tags=["users"])
async def read_user(username: str):
    """
    Retrieve a specific user by username.

    Args:
        username (str): The username of the user to retrieve

    Returns:
        dict: User information corresponding to the given username
    """
    return {"username": username}