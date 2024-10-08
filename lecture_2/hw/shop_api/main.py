from fastapi import FastAPI


from .routers.item_routers import router_item
from .routers.cart_routers import router_cart

app = FastAPI(title="Shop API")

app.include_router(router_cart)
app.include_router(router_item)
