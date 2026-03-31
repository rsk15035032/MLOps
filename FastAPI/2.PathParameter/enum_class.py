from enum import Enum
from fastapi import FastAPI


class ModelName(str, Enum):
    """
    Enum class representing the available deep learning model names.

    Why this is used:
    -----------------
    Instead of accepting any random string from the user, we restrict the
    input to only specific model names. This helps with:

    1. Input validation
    2. Better documentation in Swagger UI
    3. Avoiding invalid model names
    4. Making the API more reliable

    In this case, the allowed model names are:
    - alexnet
    - resnet
    - lenet

    Since it inherits from 'str', FastAPI treats it as a string in the URL.
    """

    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    """
    Get details about a specific deep learning model.

    Path Parameter
    --------------
    model_name : ModelName
        The name of the model provided in the URL.
        Only the following values are allowed:
        - alexnet
        - resnet
        - lenet

    How it works
    ------------
    FastAPI automatically converts the string from the URL into a ModelName
    enum value. Then we check which model was requested and return a message.

    Example Requests
    ----------------
    /models/alexnet
    /models/resnet
    /models/lenet

    Example Responses
    -----------------
    If model_name = alexnet:
        {"model_name": "alexnet", "message": "Deep Learning FTW!"}

    If model_name = lenet:
        {"model_name": "lenet", "message": "LeCNN all the images"}

    If model_name = resnet:
        {"model_name": "resnet", "message": "Have some residuals"}

    Returns
    -------
    dict
        A JSON response containing:
        - model_name : the selected model
        - message : a short description related to that model
    """

    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}