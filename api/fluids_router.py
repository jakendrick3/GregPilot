from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from ..db import db, fluids, fluidslog

router = APIRouter(
    tags=["fluids"],
    responses={404: {"description": "Not found"}}
)

@router.get("/fluids", response_model=list[fluids.Fluids])
async def get_fluids(*, session: Session = Depends(db.get_session), offset: int = 0, limit: int = Query(default=10000, le=10000)):
    returnfluids = await fluids.read_fluids(session=session, offset=offset, limit=limit)
    return returnfluids

@router.post("/fluids", response_model=list[fluids.Fluids])
async def post_fluids(*, session: Session = Depends(db.get_session), postfluids: list[fluids.Fluids]):
    return await fluids.create_fluids(session=session, fluids=postfluids)

@router.get("/fluids/log", response_model=list[fluidslog.FluidsLog])
async def get_fluids_log(*, session: Session = Depends(db.get_session), offset: int = 0, limit: int = Query(default=10000, le=10000)):
    returnfluids = await fluidslog.read_fluids_log(session=session, offset=offset, limit=limit)
    return returnfluids

@router.post("/fluids/log", response_model=list[fluidslog.FluidsLog])
async def post_fluids_log(*, session: Session = Depends(db.get_session), fluids: list[fluidslog.FluidsLogEntry]):
    return await fluidslog.create_fluids_log(session=session, fluids=fluids)