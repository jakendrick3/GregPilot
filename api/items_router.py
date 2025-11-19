from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from ..db import db, items, itemslog

router = APIRouter(
    tags=["items"],
    responses={404: {"description": "Not found"}}
)

@router.get("/items", response_model=list[items.Items])
async def get_items(*, session: Session = Depends(db.get_session), offset: int = 0, limit: int = Query(default=10000, le=10000)):
    returnitems = await items.read_items(session=session, offset=offset, limit=limit)
    return returnitems

@router.post("/items", response_model=list[items.Items])
async def post_items(*, session: Session = Depends(db.get_session), postitems: list[items.Items]):
    return await items.create_items(session=session, items=postitems)

@router.get("/items/log", response_model=list[itemslog.ItemsLog])
async def get_items_log(*, session: Session = Depends(db.get_session), offset: int = 0, limit: int = Query(default=10000, le=10000)):
    returnitems = await itemslog.read_items_log(session=session, offset=offset, limit=limit)
    return returnitems

@router.post("/items/log", response_model=list[itemslog.ItemsLog])
async def post_items_log(*, session: Session = Depends(db.get_session), items: list[itemslog.ItemsLogEntry]):
    return await itemslog.create_items_log(session=session, items=items)