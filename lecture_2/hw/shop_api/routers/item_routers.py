from http import HTTPStatus
from typing import Optional, List
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from ..models.item_models import Item, ItemRequest, ItemPatchRequest
from ..storage import create_item as cr_item, get_item as gt_item, get_items as gt_items, update_item as upd_items, patch_item as ptch_item, delete_item as dlt_item

router_item = APIRouter(prefix='/item')

@router_item.post(
    '/',
    responses={
        HTTPStatus.CREATED: {
            'description': 'Success: created new item',
        },
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            'description': 'Fail: did not create new item',
        },
    },
    status_code=HTTPStatus.CREATED,
    response_model=Item)
async def create_item(item_request: ItemRequest, response: Response) -> Item:
    try:
        item = cr_item(item_request)
        response.headers['location'] = f'/item/{item.id}'
        return item
    except ValueError:
        raise HTTPException(HTTPStatus.UNPROCESSABLE_ENTITY)


@router_item.get(
    '/{id}',
    responses={
        HTTPStatus.OK: {
            'description': 'Success',
        },
        HTTPStatus.NOT_FOUND: {
            'description': 'Fail',
        },
    },
    status_code=HTTPStatus.OK,
    response_model=Item)
async def get_item(id: int) -> Item:
    item = gt_item(id)
    if item is None or item.deleted:
        raise HTTPException(HTTPStatus.NOT_FOUND, 'Item not found')
    return item


@router_item.get(
    '/',
    responses={
        HTTPStatus.OK: {
            'description': 'Success',
        },
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            'description': 'Fail'
        },
    },
    status_code=HTTPStatus.OK,
    response_model=List[Item])
async def get_items(
    offset: Optional[int] = 0,
    limit: Optional[int] = 10,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    show_deleted: bool = False):
    try:
        items = gt_items(offset, limit, min_price, max_price, show_deleted)
    except ValueError:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY)
    return items


@router_item.put(
    '/{id}',
    responses={
        HTTPStatus.OK: {
            'description': 'Success',
        },
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            'description': 'Fail',
        },
    },
    status_code=HTTPStatus.OK,
    response_model=Item)
async def update_item(id: int, item_request: ItemRequest) -> Item:
    try:
        updated_item = upd_items(id, item_request)
    except ValueError:
        raise HTTPException(HTTPStatus.UNPROCESSABLE_ENTITY)
    return updated_item


@router_item.patch(
    '/{id}',
    responses={
        HTTPStatus.OK: {
            'description': 'Success',
        },
        HTTPStatus.NOT_MODIFIED: {
            'description': 'Fail',
        },
    },
    status_code=HTTPStatus.OK,
    response_model=Item)
async def patch_item(id: int, item_patch_request: ItemPatchRequest) -> Item:
    try:
        item = ptch_item(id, item_patch_request)
    except ValueError:
        raise HTTPException(HTTPStatus.NOT_MODIFIED)
    return item


@router_item.delete(
    '/{id}',
    responses={
        HTTPStatus.OK:
            {'description': 'Success'},
        HTTPStatus.NOT_FOUND:
            {'description': 'Fail'},
    },
    status_code=HTTPStatus.OK,
    response_model=Item)
async def delete_item(id: int):
    try:
        item = dlt_item(id)
    except Exception:
        raise HTTPException(HTTPStatus.NOT_FOUND)
    return item
