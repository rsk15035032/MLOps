from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    """
    Data model representing an item.
    """
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = Field(default_factory=list)  # ✅ fixed


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get(
    "/items/{item_id}",
    response_model=Item,
    response_model_exclude_unset=True
)
async def read_item(item_id: str):
    """
    Retrieve an item by ID.

    Args:
        item_id (str): Unique identifier of the item.

    Returns:
        Item: Item data.

    Raises:
        HTTPException: If item is not found.
    """
    item = items.get(item_id)  # ✅ safe access

    if item is None:
        raise HTTPException(
            status_code=404,
            detail=f"Item '{item_id}' not found"
        )

    return item