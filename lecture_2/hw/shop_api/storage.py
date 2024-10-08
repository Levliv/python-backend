from typing import List, Optional
from .models.cart_models import Cart, CartItem
from .models.item_models import Item, ItemRequest, ItemPatchRequest

__carts = dict[int, Cart]()
__items = dict[int, Item]()

id_generator = (i for i in range(999999))

def create_cart() -> Cart:
    cart = Cart(id=next(id_generator))
    __carts[cart.id] = cart
    return cart

def get_cart(cart_id: int) -> Optional[Cart]:
    return __carts.get(cart_id)

def get_carts(
    offset: int,
    limit: int,
    min_price: Optional[float],
    max_price: Optional[float],
    min_quantity: Optional[int],
    max_quantity: Optional[int],
) -> Optional[List[Cart]]:
    carts = list(__carts.values())

    if not carts:
        return None

    carts = [
        cart
        for cart in carts
        if ((min_price is None) or (cart.price >= min_price))
        and ((max_price is None) or (cart.price <= max_price))
    ]

    if min_quantity is not None:
        carts = [
            cart
            for cart in carts
            if sum(item.quantity for item in cart.items) >= min_quantity
        ]

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
        raise ValueError(f"{cart_id if cart_id is None else item_id } not found.")

    for cart_item in cart.items:
        if cart_item.id == item_id:
            cart_item.quantity += 1
            break
    else:
        cart.items.append(
            CartItem(id=item.id, name=item.name, quantity=1, available=True)
        )

    cart.price += item.price

    return cart

def create_item(item_request: ItemRequest) -> Item:
    item = Item(id=next(id_generator), name=item_request.name, price=item_request.price)
    __items[item.id] = item
    return item

def get_item(item_id: int) -> Optional[Item]:
    return __items.get(item_id)

def get_items(
    offset: int,
    limit: int,
    min_price: Optional[float],
    max_price: Optional[float],
    show_deleted: bool,
) -> Optional[List[Item]]:
    if offset < 0 or limit <= 0:
        raise ValueError('Non-negative values required for offset and limit')

    if (min_price is not None and min_price < 0) or (max_price is not None and max_price < 0):
        raise ValueError('Price must be non-negative')

    items = [
        item
        for item in __items.values()
        if ((min_price is None) or (item.price >= min_price))
        and ((max_price is None) or (item.price <= max_price))
        and (show_deleted or (not item.deleted))
    ]
    return items[offset:offset + limit]

def update_item(item_id: int, item_request: ItemRequest) -> Optional[Item]:
    item = get_item(item_id)

    if item is None or item.deleted:
        return None
    item.name = item_request.name
    item.price = item_request.price
    return item

def patch_item(item_id: int, item_patch_request: ItemPatchRequest) -> Optional[Item]:
    item = get_item(item_id)
    if item is None or item.deleted:
        return None

    if item_patch_request.name is not None:
        item.name = item_patch_request.name
    if item_patch_request.price is not None:
        item.price = item_patch_request.price

    return item

def delete_item(item_id: int) -> Optional[Item]:
    item = __items.get(item_id)
    if item is None:
        return None

    item.deleted = True
    return item
