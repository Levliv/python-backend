from pydantic import BaseModel
from typing import List


class CartItem(BaseModel):
    id: int
    name: str
    quantity: int = 1
    available: bool = True

class Cart(BaseModel):
    id: int
    items: List[CartItem] = []
    price: float = 0.0

class CartRequest(BaseModel):
    item_id: int
