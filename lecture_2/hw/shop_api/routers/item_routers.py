from http import HTTPStatus
from typing import Optional, List

from fastapi import APIRouter, HTTPException, Query
from pydantic.v1 import NotNoneError

from ..models.item_models import Item, ItemRequest, ItemPatchRequest
from ..storage import create_item as cr_item, get_item as gt_item, get_items as gt_items, update_item as upd_items, patch_item as ptch_item, delete_item as dlt_item
from starlette.responses import Response

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
    response_model=Item,
)
async def create_item(item_request: ItemRequest, response: Response) -> Item:
    try:
        item = cr_item(item_request)
        response.headers['location'] = f'/item/{item.id}'
        return item
    except ValueError as e:
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
    response_model=Item,
)
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
            'description': 'Fail: can not process request'
        },
    },
    status_code=HTTPStatus.OK,
    response_model=List[Item],
)
async def get_items(
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    show_deleted: bool = False,
):
    if offset is None:
        offset = 0
    if limit is None:
        limit = 10
    try:
        items = gt_items(offset, limit, min_price, max_price, show_deleted)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY)
    return items


@router_item.put(
    '/{id}',
    responses={
        HTTPStatus.OK: {
            'description': 'Successfully changed data of item',
        },
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            'description': 'Failed to changed data of item',
        },
    },
    status_code=HTTPStatus.OK,
    response_model=Item,
)
async def update_item(id: int, item_request: ItemRequest) -> Item:
    try:
        updated_item = upd_items(id, item_request)
        if updated_item is None:
            raise HTTPException(HTTPStatus.NOT_FOUND, 'Item not found')
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))
    return updated_item


@router_item.patch(
    '/{id}',
    responses={
        HTTPStatus.OK: {
            'description': 'Success: modified data of item',
        },
        HTTPStatus.NOT_MODIFIED: {
            'description': 'Fail: did not modify data of item',
        },
    },
    status_code=HTTPStatus.OK,
    response_model=Item,
)
async def patch_item(id: int, item_patch_request: ItemPatchRequest) -> Item:
    try:
        item = ptch_item(id, item_patch_request)
        if item is None:
            raise HTTPException(HTTPStatus.NOT_FOUND, 'Item was deleted or not found')
    except Exception as e:
        raise HTTPException(HTTPStatus.NOT_MODIFIED)
    return item


@router_item.delete(
    '/{id}',
    responses={
        HTTPStatus.OK: {'description': 'Successfully deleted item'},
        HTTPStatus.NOT_FOUND: {'description': 'Failed to delete item'},
    },
    status_code=HTTPStatus.OK,
)
async def delete_item(id: int):
    try:
        item = dlt_item(id)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
    return item
'''from fastapi import APIRouter, HTTPException
from http import HTTPStatus

from fastapi.responses import JSONResponse
from ..models.item_models import Item, ItemRequest
from ..storage import create_item, get_item

router_item = APIRouter(prefix='/item')

@router_item.post(
    '/',
          responses={
              HTTPStatus.CREATED: {
                  'description': 'Successfully created new item',
              },
              HTTPStatus.UNPROCESSABLE_ENTITY: {
                  'description': 'Failed to create new item. Something went wrong',
              },
          },
          status_code=HTTPStatus.CREATED,
          response_model=int)
def add_item(item_request: ItemRequest):
    item = create_item(item_request)
    return JSONResponse(content={'id': item.id, 'price': item.price, 'name': item.name}, status_code=HTTPStatus.CREATED, headers={'location': f'/item/{item.id}'})

@router_item.get('/{id}',
                 responses={
                     HTTPStatus.OK: {
                         'description': 'Successfully returned requested item',
                     },
                     HTTPStatus.NOT_FOUND: {
                         'description': 'Failed to return requested item as one was not found',
                     },
                 },
                 status_code=HTTPStatus.OK,
                 response_model=Item)
def get_item_by_id(item_id: int):
    item = get_item(item_id)
    if item is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Item was not found')
    return JSONResponse(content={'id': item.id, 'price': item.price, 'name': item.name}, status_code=HTTPStatus.Ok, headers={'location': f'/item/{item.id}'})

@router_item.get('/')
def get_query_items(
        offset: int = 0,
        limit: int = 10,
        min_price: int = None,
        max_price: int = None,
        show_deleted: bool = False):
    return None

@router_item.put('/{id}')
def change_item_by_id(id: int):
    return None

@router_item.patch('/{id}')
def update_item_by_id(id: int):
    return None

@router_item.delete('/{id}')
def delete_item_by_id(id: int):
    return None
'''