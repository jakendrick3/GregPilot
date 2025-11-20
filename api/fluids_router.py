from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from ..db import db, fluids, fluidslog, fluidsinv

router = APIRouter(
    tags=["fluids"],
    responses={404: {"description": "Not found"}}
)

@router.get("/api/fluids", response_model=list[fluids.Fluids])
async def get_fluids(*, session: Session = Depends(db.get_session), offset: int = 0, limit: int = Query(default=10000, le=10000)):
    returnfluids = await fluids.read_fluids(session=session, offset=offset, limit=limit)
    return returnfluids

@router.post("/api/fluids", response_model=list[fluids.Fluids])
async def post_fluids(*, session: Session = Depends(db.get_session), postfluids: list[fluids.Fluids]):
    return await fluids.create_fluids(session=session, fluids=postfluids)

@router.get("/api/fluids/log", response_model=list[fluidslog.FluidsLog])
async def get_fluids_log(*, session: Session = Depends(db.get_session), offset: int = 0, limit: int = Query(default=10000, le=10000)):
    returnfluids = await fluidslog.read_fluids_log(session=session, offset=offset, limit=limit)
    return returnfluids

@router.post("/api/fluids/log", response_model=list[fluidslog.FluidsLog])
async def post_fluids_log(*, session: Session = Depends(db.get_session), fluids: list[fluidslog.FluidsLogEntry]):
    return await fluidslog.create_fluids_log(session=session, fluids=fluids)

@router.get("/api/fluids/inv", response_model=list[fluidsinv.FluidsInv])
async def get_fluids_log(*, session: Session = Depends(db.get_session)):
    returnfluids = await fluidsinv.read_fluids_inv(session=session)
    return returnfluids