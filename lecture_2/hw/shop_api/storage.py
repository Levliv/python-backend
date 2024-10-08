from typing import List, Optional
from .models.cart_models import Cart, CartItem
from .models.item_models import Item, ItemRequest, ItemPatchRequest

__carts = dict[int, Cart]()
__items = dict[int, Item]()

id_generator = (i for i in range(999999))

def create_cart() -> Cart:
    cart = Cart(id=next(id_generator))
    __carts.update({cart.id: cart})
    return cart

def get_cart(id: int) -> Optional[Cart]:
    return __carts.get(id)

def get_carts(
    offset: int,
    limit: int,
    min_price: Optional[float],
    max_price: Optional[float],
    min_quantity: Optional[int],
    max_quantity: Optional[int]) -> Optional[List[Cart]]:
    if offset < 0 or limit <= 0:
        raise ValueError

    params = [min_price, max_price, min_quantity, max_quantity]
    for param in params:
        if param is not None and param < 0:
            raise ValueError

    carts = [cart for cart in __carts.values()
             if (min_price is None or cart.price >= min_price) and (max_price is None or cart.price <= max_price)]

    if min_quantity is not None:
        carts = [cart for cart in carts if sum(item.quantity for item in cart.items) >= min_quantity]

    if max_quantity is not None:
        carts = [
            cart
            for cart in carts
            if sum(item.quantity for item in cart.items) <= max_quantity
        ]

    return carts[offset : offset + limit]

def add_item_to_cart(cart_id: int, item_id: int) -> Cart:
    cart = get_cart(cart_id)
    item = get_item(item_id)
    if cart is None or item is None:
        raise ValueError


    for cart_item in cart.items:
        if cart_item.id == item_id:
            cart_item.quantity += 1
            cart.price += item.price
            return cart

    cart.items.append(CartItem(id=item.id, name=item.name))
    cart.price += item.price
    return cart

def create_item(item_request: ItemRequest) -> Item:
    item = Item(id=next(id_generator), name=item_request.name, price=item_request.price)
    __items[item.id] = item
    return item

def get_item(id: int) -> Optional[Item]:
    return __items.get(id)

def get_items(
    offset: int,
    limit: int,
    min_price: Optional[float],
    max_price: Optional[float],
    show_deleted: bool) -> Optional[List[Item]]:
    if offset < 0 or limit <= 0:
        raise ValueError

    if (min_price is not None and min_price < 0) or (max_price is not None and max_price < 0):
        raise ValueError

    items = [item for item in __items.values() if ((min_price is None) or (item.price >= min_price))
        and ((max_price is None) or (item.price <= max_price)) and (show_deleted or (not item.deleted))]
    return items[offset:offset + limit]

def patch_item(id: int, item_patch_request: ItemPatchRequest) -> Optional[Item]:
    item = get_item(id)
    if item is None or item.deleted:
        raise ValueError

    if item_patch_request.name is not None:
        item.name = item_patch_request.name
    if item_patch_request.price is not None:
        item.price = item_patch_request.price

    return item

def update_item(id: int, item_request: ItemRequest) -> Optional[Item]:
    return patch_item(id, ItemPatchRequest(name=item_request.name, price=item_request.price))

def delete_item(id: int) -> Optional[Item]:
    item = __items.get(id)
    if item is None:
        raise ValueError

    item.deleted = True
    return item
