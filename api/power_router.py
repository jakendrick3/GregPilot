from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from ..db import db, powerlog, power, paginate

router = APIRouter(
    tags=["power"],
    responses={404: {"description": "Not found"}}
)

@router.get("/api/power/log", response_model=list[powerlog.PowerLog])
async def get_power_log(*, session: Session = Depends(db.get_session), paginate: paginate.Paginate = Depends(), filter: powerlog.PowerFilter = Depends()):
    returnlogs = await powerlog.read_power_log(session=session, offset=offset, limit=limit)
    return returnlogs

@router.post("/api/power/log", response_model=powerlog.PowerLog)
async def post_power_log(*, session: Session = Depends(db.get_session), entry: powerlog.PowerLogEntry):
    return await powerlog.create_power_log(session=session, entry=entry)

@router.get("/api/power", response_model=power.Power)
async def get_power(*, session: Session = Depends(db.get_session)):
    returnpower = await power.read_power(session=session)
    return returnpower