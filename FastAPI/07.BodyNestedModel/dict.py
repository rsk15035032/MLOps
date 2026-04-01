from fastapi import FastAPI

# Create FastAPI application
app = FastAPI()


@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    """
    Create Index Weights API

    This endpoint accepts a dictionary directly in the request body.

    Important Concept Demonstrated
    ------------------------------
    Instead of sending a JSON object with named fields (like a model),
    here we send a dictionary where:

        key   -> integer (index number)
        value -> float (weight value)

    FastAPI automatically:
    - Reads the JSON request body
    - Converts the keys into integers
    - Converts the values into floats
    - Validates the data types

    Parameters
    ----------
    weights : dict[int, float]
        A dictionary where:
        - key represents an index (integer)
        - value represents a weight (float)

    Returns
    -------
    dict[int, float]
        Returns the same dictionary after validation.

    Example Request
    ---------------
    POST /index-weights/

    {
      "1": 0.25,
      "2": 0.35,
      "3": 0.40
    }

    Note:
    In JSON, keys must always be strings.
    FastAPI automatically converts them into integers.

    Example Response
    ----------------
    {
      "1": 0.25,
      "2": 0.35,
      "3": 0.40
    }
    """

    return weights