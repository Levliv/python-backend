from fastapi import FastAPI
from .routers.item_routers import router_item
from .routers.cart_routers import router_cart
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Shop API")

Instrumentator().instrument(app).expose(app)

app.include_router(router_cart)
app.include_router(router_item)
