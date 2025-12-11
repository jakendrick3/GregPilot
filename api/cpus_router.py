from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from ..db import db, cpus

router = APIRouter(
    tags=["cpus"],
    responses={404: {"description": "Not found"}}
)

@router.get("/api/cpus", response_model=list[cpus.CPU])
async def get_cpus(*, session: Session = Depends(db.get_session), offset: int = 0, limit: int = Query(default=10000, le=10000)):
    returncpus = await cpus.read_cpus(session=session, offset=offset, limit=limit)
    return returncpus

@router.post("/api/cpus", response_model=list[cpus.CPU])
async def post_cpus(*, session: Session = Depends(db.get_session), postcpus: list[cpus.CPUPublic]):
    return await cpus.create_cpus(session=session, cpus=postcpus)