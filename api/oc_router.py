from fastapi import APIRouter, Depends, Request
from sqlmodel import Session, select
from ..db import db, items, itemslog, fluids, fluidslog, powerlog
from slpp import slpp as lua

router = router = APIRouter(
    tags=["OpenComputers"],
    responses={404: {"description": "Not found"}}
)

def unserialize(raw: str):
    if raw.startswith('"') and raw.endswith('"'):
        raw = raw[1:-1]
    raw = raw.replace('\\"', '"')

    result = lua.decode(raw)

    return result

@router.post("/api/oc/items")
async def post_oc_items(*, session: Session = Depends(db.get_session), request: Request):
    body_bytes = await request.body()
    body_str = body_bytes.decode("utf-8")
    data = unserialize(body_str)

    passids = []
    passlogs = []
    for entry in data:
        itemid = entry["id"] + entry["damage"]
        newid = {
            'id': itemid,
            'name': entry["name"]
        }

        newlog = {
            'id': itemid,
            'size': entry["size"]
        }
    
        newid = items.Items.model_validate(newid)
        newlog = itemslog.ItemsLogEntry.model_validate(newlog)

        passids.append(newid)
        passlogs.append(newlog)
    
    await items.create_items(session=session, items=passids)
    await itemslog.create_items_log(session=session, items=passlogs)
    return

@router.post("/api/oc/fluids")
async def post_oc_fluids(*, session: Session = Depends(db.get_session), request: Request):
    body_bytes = await request.body()
    body_str = body_bytes.decode("utf-8")
    data = unserialize(body_str)

    passids = []
    passlogs = []
    for entry in data:
        newid = {
            'id': entry["id"],
            'name': entry["name"]
        }

        newlog = {
            'id': entry["id"],
            'amount': entry["amount"]
        }
    
        newid = fluids.Fluids.model_validate(newid)
        newlog = fluidslog.FluidsLogEntry.model_validate(newlog)

        passids.append(newid)
        passlogs.append(newlog)
    
    await fluids.create_fluids(session=session, fluids=passids)
    await fluidslog.create_fluids_log(session=session, fluids=passlogs)
    return

@router.post("/api/oc/power")
async def post_oc_power(*, session: Session = Depends(db.get_session), request: Request):
    body_bytes = await request.body()
    body_str = body_bytes.decode("utf-8")
    data = unserialize(body_str)

    newlog = powerlog.PowerLogEntry.model_validate(data)
        
    await powerlog.create_power_log(session=session, entry=newlog)
    return