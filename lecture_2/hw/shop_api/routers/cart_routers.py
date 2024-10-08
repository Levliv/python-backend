from http import HTTPStatus
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from ..models.cart_models import CartResponse
from ..storage import create_cart as crt_cart, get_cart as gt_cart, get_carts as gt_carts, add_item_to_cart as ad_item_to_cart
from fastapi.responses import Response

router_cart = APIRouter(prefix='/cart')


@router_cart.post(
    '/',
    responses={
        HTTPStatus.CREATED: {
            'description': 'Success: created new empty cart',
        },
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            'description': 'Fail: did not create new empty cart',
        },
    },
    status_code=HTTPStatus.CREATED,
    response_model=CartResponse,
)
async def create_cart(response: Response) -> CartResponse:
    try:
        cart = crt_cart()
        response.headers['location'] = f'/cart/{cart.id}'
        return cart
    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))


@router_cart.get(
    '/{cart_id}',
    responses={
        HTTPStatus.OK: {
            'description': 'Successfully returned requested cart',
        },
        HTTPStatus.NOT_FOUND: {
            'description': 'Failed to return requested cart as one was not found',
        },
    },
    status_code=HTTPStatus.OK,
    response_model=CartResponse,
)
async def get_cart(cart_id: int) -> CartResponse:
    try:
        cart = gt_cart(cart_id)
        if cart is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Cart not found'
            )
    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))
    return cart


@router_cart.get(
    '/',
    responses={
        HTTPStatus.OK: {
            'description': 'Successfully returned list of carts',
        },
        HTTPStatus.NOT_FOUND: {
            'description': 'Failed to return any carts for theese params',
        },
    },
    status_code=HTTPStatus.OK,
    response_model=List[CartResponse],
)
async def get_carts(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    min_quantity: Optional[int] = Query(None, ge=0),
    max_quantity: Optional[int] = Query(None, ge=0),
) -> List[CartResponse]:
    try:
        carts = gt_carts(
            offset, limit, min_price, max_price, min_quantity, max_quantity
        )
        if carts is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail='Carts not found'
            )
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))
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
    response_model=CartResponse,
)
async def add_item_to_cart(cart_id: int, item_id: int) -> CartResponse:
    try:
        cart = ad_item_to_cart(cart_id, item_id)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))
    return cart