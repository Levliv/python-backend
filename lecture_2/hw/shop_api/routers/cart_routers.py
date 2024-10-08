from http import HTTPStatus
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from ..models.cart_models import Cart
from ..storage import create_cart as crt_cart, get_cart as gt_cart, get_carts as gt_carts, add_item_to_cart as ad_item_to_cart

router_cart = APIRouter(prefix='/cart')

@router_cart.post(
    '/',
    responses={
        HTTPStatus.CREATED: {
            'description': 'Success',
        },
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            'description': 'Fail',
        },
    },
    status_code=HTTPStatus.CREATED,
    response_model=Cart)
async def create_cart(response: Response) -> Cart:
    try:
        cart = crt_cart()
        response.headers['location'] = f'/cart/{cart.id}'
        return cart
    except ValueError:
        raise HTTPException(HTTPStatus.UNPROCESSABLE_ENTITY)


@router_cart.get(
    '/{cart_id}',
    responses={
        HTTPStatus.OK: {
            'description': 'Success',
        },
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            'description': 'Fail',
        },
    },
    status_code=HTTPStatus.OK,
    response_model=Cart)
async def get_cart(cart_id: int) -> Cart:
    try:
        cart = gt_cart(cart_id)
    except ValueError:
        raise HTTPException(HTTPStatus.UNPROCESSABLE_ENTITY)
    return cart


@router_cart.get(
    '/',
    responses={
        HTTPStatus.OK: {
            'description': 'Success',
        },
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            'description': 'Fail',
        },
    },
    status_code=HTTPStatus.OK,
    response_model=List[Cart])
async def get_carts(
    offset: Optional[int] = 0,
    limit: Optional[int] = 10,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_quantity: Optional[int] = None,
    max_quantity: Optional[int] = None) -> List[Cart]:
    try:
        carts = gt_carts(
            offset, limit, min_price, max_price, min_quantity, max_quantity
        )
    except ValueError:
        raise HTTPException(HTTPStatus.UNPROCESSABLE_ENTITY)
    return carts


@router_cart.post(
    '/{cart_id}/add/{item_id}',
    responses={
        HTTPStatus.CREATED: {
            'description': 'Successfully added item to cart',
        },
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            'description': 'Failed to add item to cart. Something went wrong',
        },
    },
    status_code=HTTPStatus.CREATED,
    response_model=Cart)
async def add_item_to_cart(cart_id: int, item_id: int) -> Cart:
    try:
        cart = ad_item_to_cart(cart_id, item_id)
    except ValueError:
        raise HTTPException(HTTPStatus.UNPROCESSABLE_ENTITY)
    return cart