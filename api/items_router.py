from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from ..db import db, items, itemslog, itemsinv, paginate

router = APIRouter(
    tags=["items"],
    responses={404: {"description": "Not found"}}
)

@router.get("/api/items", response_model=list[items.Items])
async def get_items(*, session: Session = Depends(db.get_session), paginate: paginate.Paginate = Depends(), filter: items.ItemsFilter = Depends()):
    returnitems = await items.read_items(session=session, paginate=paginate, filter=filter)
    return returnitems

@router.post("/api/items", response_model=list[items.Items])
async def post_items(*, session: Session = Depends(db.get_session), postitems: list[items.Items]):
    return await items.create_items(session=session, items=postitems)

@router.get("/api/items/log", response_model=list[itemslog.ItemsLog])
async def get_items_log(*, session: Session = Depends(db.get_session), paginate: paginate.Paginate = Depends(), filter: itemslog.ItemsLogFilter = Depends()):
    returnitems = await itemslog.read_items_log(session=session, paginate=paginate, filter=filter)
    return returnitems

@router.post("/api/items/log", response_model=list[itemslog.ItemsLog])
async def post_items_log(*, session: Session = Depends(db.get_session), items: list[itemslog.ItemsLogEntry]):
    return await itemslog.create_items_log(session=session, items=items)

@router.get("/api/items/inv", response_model=list[itemsinv.ItemsInv])
async def get_items_log(*, session: Session = Depends(db.get_session), paginate: paginate.Paginate = Depends(), filter: itemsinv.ItemsInvFilter = Depends()):
    returnitems = await itemsinv.read_items_inv(session=session, filter=filter)
    return returnitems