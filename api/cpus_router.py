from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from ..db import db, cpus, paginate

router = APIRouter(
    tags=["cpus"],
    responses={404: {"description": "Not found"}}
)

@router.get("/api/cpus", response_model=list[cpus.CPU])
async def get_cpus(*, session: Session = Depends(db.get_session), paginate: paginate.Paginate = Depends(), filter: cpus.CPUFilter = Depends()):
    returncpus = await cpus.read_cpus(session=session, paginate=paginate, filter=filter)
    return returncpus

@router.post("/api/cpus", response_model=list[cpus.CPU])
async def post_cpus(*, session: Session = Depends(db.get_session), postcpus: list[cpus.CPUPublic]):
    return await cpus.create_cpus(session=session, cpus=postcpus)