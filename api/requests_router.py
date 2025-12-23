from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from ..db import db, craft, craftables, paginate

router = APIRouter(
    tags=["requests"],
    responses={404: {"description": "Not found"}}
)

@router.get("/api/requests/craft", response_model=list[craft.CraftRequest])
async def get_craft_requests(*, session: Session = Depends(db.get_session), paginate: paginate.Paginate = Depends(), filter: craft.CraftRequestFilter = Depends()):
    returncrafts = await craft.read_craftrequests(session=session, paginate=paginate, filter=filter)
    return returncrafts

@router.post("/api/requests/craft", response_model=list[craft.CraftRequestPublic])
async def post_crafts(*, session: Session = Depends(db.get_session), postcrafts: list[craft.CraftRequestPublic]):
    validatedrequests = []
    for craftrequest in postcrafts:
        if craftrequest.type == "fluid":
            check = session.exec(select(craftables.Craftable).where(craftables.Craftable.fluidid == craftrequest.id)).first()
            if check is not None:
                validatedrequests.append(craftrequest)
        elif craftrequest.type == "item":
            check = session.exec(select(craftables.Craftable).where(craftables.Craftable.itemid == craftrequest.id)).first()
            if check is not None:
                validatedrequests.append(craftrequest)
    returnstr = await craft.create_craftrequests(session=session, crafts=validatedrequests)
    return returnstr