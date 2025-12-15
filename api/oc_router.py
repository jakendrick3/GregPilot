from fastapi import APIRouter, Depends, Request
from sqlmodel import Session, select
from ..db import db, items, itemslog, fluids, fluidslog, powerlog, essentia, essentialog, cpus, craftables, craft
from slpp import slpp as lua

router = router = APIRouter(
    tags=["OpenComputers"],
    responses={404: {"description": "Not found"}}
)

def unserialize(raw: str):
    if raw.startswith('"') and raw.endswith('"'):
        raw = raw[1:-1]
    raw = raw.replace('\\"', '"')
    raw = raw.encode("ascii", errors="ignore").decode("ascii")

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
        itemid = entry["id"] + ";" + entry["damage"]
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

@router.post("/api/oc/essentia")
async def post_oc_essentia(*, session: Session = Depends(db.get_session), request: Request):
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
    
        newid = essentia.Essentia.model_validate(newid)
        newlog = essentialog.EssentiaLogEntry.model_validate(newlog)

        passids.append(newid)
        passlogs.append(newlog)
    
    await essentia.create_essentia(session=session, essentia=passids)
    await essentialog.create_essentia_log(session=session, essentia=passlogs)
    return

@router.post("/api/oc/cpus")
async def post_oc_cpus(*, session: Session = Depends(db.get_session), request: Request):
    body_bytes = await request.body()
    body_str = body_bytes.decode("utf-8")
    data = unserialize(body_str)

    newcpus = []
    for cpu in data:
        newcpu = cpus.CPUPublic.model_validate(cpu)
        newcpus.append(newcpu)
        
    await cpus.create_cpus(session=session, cpus=newcpus)
    return

@router.post("/api/oc/craftables")
async def post_oc_craftables(*, session: Session = Depends(db.get_session), request: Request):
    body_bytes = await request.body()
    body_str = body_bytes.decode("utf-8")
    data = unserialize(body_str)

    passitems = []
    passfluids = []
    passcrafts = []

    for entry in data:
        if entry["type"] == "item":
            itemid = str(entry["id"]) + ";" + str(entry["damage"])
            newitem = {
                'id': itemid,
                'name': entry["name"]
            }
            newitem = items.Items.model_validate(newitem)
            passitems.append(newitem)

            newcraft = {
                'itemid': itemid,
                'type': "item"
            }
            newcraft = craftables.CraftablePublic.model_validate(newcraft)
            passcrafts.append(newcraft)
        elif entry["type"] == "fluid":
            newfluid = {
                'id': entry["id"],
                'name': entry["name"]
            }
            newfluid = fluids.Fluids.model_validate(newfluid)
            passfluids.append(newfluid)

            newcraft = {
                'fluidid': entry["id"],
                'type': "fluid"
            }
            newcraft = craftables.CraftablePublic.model_validate(newcraft)
            passcrafts.append(newcraft)
        else:
            continue
    
    await items.create_items(session=session, items=passitems)
    await fluids.create_fluids(session=session, fluids=passfluids)
    await craftables.create_craftables(session=session, crafts=passcrafts)
    return

@router.post("/api/oc/craft")
async def post_oc_crafts(*, session: Session = Depends(db.get_session), request: Request):
    body_bytes = await request.body()
    body_str = body_bytes.decode("utf-8")
    data = unserialize(body_str)

    patchcrafts = []
    for record in data:
        refitem = session.exec(select(craft.CraftRequest).where(craft.CraftRequest.requestid == record["requestid"])).first()
        refitem.status = record["status"]
        patchcrafts.append(refitem)

    await craft.update_craftrequests(session=session, crafts=patchcrafts)
    return