from enum import Enum

from fastapi import FastAPI, HTTPException, Path, Query, Body
from typing import Annotated
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = FastAPI()

items = {0:Item(name="Keyboard", description="Full size computer keyboard", price=19.99)}

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/")
async def read_items( name: Annotated[str, None] = None, price: Annotated[float, None] = None):
    
    filtered_items = [i for i in items.values()]
    # Filter by price
    if price is not None:
        filtered_items = [item for item in filtered_items if item.price == price]

    # Filter by name if provided
    if name is not None:
        filtered_items = [item for item in filtered_items if name.lower() == item.name.lower()]

    return filtered_items
 

@app.post("/item/")
async def create_item(item: Item) -> Item:
    last_id = [k for k in items.keys()][-1]
    items[last_id+1] = item
    return item

@app.put("/item/{item_id}")
async def update_item( 
    item_id: int, 
    name: str | None = None,
    description: str | None = None,
    price: float | None = None,
    tax: float | None = None
    ) -> dict[str, Item]:

    if item_id not in items:
        raise HTTPException(404, f"Items with id {item_id} not found")
    
    item = items[item_id]
    if name is not None:
        item.name = name
    if description is not None:
        item.description = description
    if price is not None:
        item.price = price
    if tax is not None:
        item.tax = tax
    return {"updated": item}

@app.delete("/item/{item_id}")
async def update_item(item_id: int) -> dict[str, Item]:
    if item_id not in items:
        raise HTTPException(404, f"Items with id {item_id} not found")
    return {"deleted": items.pop(item_id)}