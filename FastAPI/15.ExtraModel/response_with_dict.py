from fastapi import FastAPI

app = FastAPI()


@app.get("/keyword-weights/", response_model=dict[str, float])
async def read_keyword_weights():
    """
    Retrieve keyword weights.

    Returns:
        dict[str, float]: A dictionary where:
            - key (str): Keyword name
            - value (float): Weight associated with the keyword

    Note:
        FastAPI validates:
        - All keys must be strings
        - All values must be floats
    """
    return {"foo": 2.3, "bar": 3.4}  # Example keyword-weight mapping