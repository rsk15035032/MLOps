from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

# Create FastAPI application
app = FastAPI()


class Image(BaseModel):
    """
    Image Model

    This model represents a single image object.

    FastAPI uses Pydantic models to:
    - Validate JSON data coming from the request body
    - Convert JSON into Python objects
    - Automatically generate API documentation (Swagger UI)

    Attributes
    ----------
    url : HttpUrl
        A valid image URL. Pydantic automatically checks whether
        the URL starts with http:// or https://

    name : str
        Name of the image.
    """

    url: HttpUrl
    name: str


@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    """
    Create Multiple Images API

    This endpoint accepts a list of Image objects directly in the request body.

    Important Concept Demonstrated
    ------------------------------
    Usually we send a dictionary in the request body.
    But here we are sending a LIST directly.

    Instead of:
        { "images": [ {...}, {...} ] }

    We send:
        [ {...}, {...} ]

    How FastAPI processes this
    --------------------------
    - FastAPI reads the JSON request body
    - Converts each object in the list into an Image model
    - Validates every image (URL must be valid, name must be string)
    - If everything is valid, it returns the list

    Parameters
    ----------
    images : list[Image]
        A list of image objects received in the request body.

    Returns
    -------
    list[Image]
        Returns the same list of validated images.

    Example Request
    ---------------
    POST /images/multiple/

    [
      {
        "url": "https://example.com/image1.png",
        "name": "Front View"
      },
      {
        "url": "https://example.com/image2.png",
        "name": "Back View"
      }
    ]

    Example Response
    ----------------
    The API returns the same validated list of images.
    """

    return images