from typing import Annotated

from fastapi import FastAPI, Form
from pydantic import BaseModel

app = FastAPI()


class FormData(BaseModel):
    """
    Schema for login form data.

    Attributes:
        username (str): Username submitted via form.
        password (str): Password submitted via form.

    Config:
        extra = "forbid":
            - Disallows any extra fields not defined in the model.
            - Raises validation error if unexpected fields are sent.
    """
    username: str
    password: str

    # Forbid extra fields in incoming form data
    model_config = {"extra": "forbid"}


@app.post("/login/")
async def login(data: Annotated[FormData, Form()]):
    """
    Handle login using form data mapped to a Pydantic model.

    Args:
        data (FormData): Parsed and validated form data.

    Returns:
        FormData: Echoes back the validated form data.

    Note:
        - `Form()` binds form data to the Pydantic model
        - Validation is automatically handled by Pydantic
        - Extra fields will raise an error due to `extra="forbid"`
    """
    return data  # Returns validated form data