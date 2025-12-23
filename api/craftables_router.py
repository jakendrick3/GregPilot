from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from ..db import db, craftables, paginate

router = APIRouter(
    tags=["craftables"],
    responses={404: {"description": "Not found"}}
)

@router.get("/api/craftables", response_model=list[craftables.Craftable])
async def get_craftables(*, session: Session = Depends(db.get_session), paginate: paginate.Paginate = Depends(), filter: craftables.CraftableFilter = Depends()):
    returncrafts = await craftables.read_craftables(session=session, paginate=paginate, filter=filter)
    return returncrafts

@router.post("/api/craftables", response_model=list[craftables.Craftable])
async def post_crafts(*, session: Session = Depends(db.get_session), postcrafts: list[craftables.CraftablePublic]):
    return await craftables.create_craftables(session=session, crafts=postcrafts)