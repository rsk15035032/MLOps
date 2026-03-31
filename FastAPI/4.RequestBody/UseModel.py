from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    """
    Pydantic model representing an item.

    Attributes
    ----------
    name : str
        Name of the item.

    description : str | None, optional
        Description of the item. Default is None.

    price : float
        Base price of the item.

    tax : float | None, optional
        Tax value applied to the item. Default is None.
    """
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    """
    Create an item and optionally calculate price including tax.

    This endpoint receives item data in the request body and returns
    the same data. If a tax value is provided, it also calculates and
    returns the final price including tax.

    Parameters
    ----------
    item : Item
        Item data sent in the request body. The data must match the
        structure defined in the Item Pydantic model.

    Returns
    -------
    dict
        A dictionary containing the item data. If tax is provided,
        an additional field `price_with_tax` will be included.

    Example
    -------
    POST /items/

    Request Body:
    {
        "name": "Laptop",
        "description": "Gaming laptop",
        "price": 70000,
        "tax": 5000
    }

    Response:
    {
        "name": "Laptop",
        "description": "Gaming laptop",
        "price": 70000,
        "tax": 5000,
        "price_with_tax": 75000
    }
    """
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict