from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from ..db import db, essentia, essentialog, essentiainv, paginate

router = APIRouter(
    tags=["essentia"],
    responses={404: {"description": "Not found"}}
)

@router.get("/api/essentia", response_model=list[essentia.Essentia])
async def get_essentia(*, session: Session = Depends(db.get_session), paginate: paginate.Paginate = Depends(), filter: essentia.EssentiaFilter = Depends()):
    returnessentia = await essentia.read_essentia(session=session, paginate=paginate, filter=filter)
    return returnessentia

@router.post("/api/essentia", response_model=list[essentia.Essentia])
async def post_essentia(*, session: Session = Depends(db.get_session), postessentia: list[essentia.Essentia]):
    return await essentia.create_essentia(session=session, essentia=postessentia)

@router.get("/api/essentia/log", response_model=list[essentialog.EssentiaLog])
async def get_essentia_log(*, session: Session = Depends(db.get_session), paginate: paginate.Paginate = Depends(), filter: essentialog.EssentiaLogFilter = Depends()):
    returnessentia = await essentialog.read_essentia_log(session=session, paginate=paginate, filter=filter)
    return returnessentia

@router.post("/api/essentia/log", response_model=list[essentialog.EssentiaLog])
async def post_essentia_log(*, session: Session = Depends(db.get_session), essentia: list[essentialog.EssentiaLog]):
    return await essentialog.create_essentia_log(session=session, essentia=essentia)

@router.get("/api/essentia/inv", response_model=list[essentiainv.EssentiaInv])
async def get_essentia_log(*, session: Session = Depends(db.get_session), filter: essentiainv.EssentiaInvFilter = Depends()):
    returnessentia = await essentiainv.read_essentia_inv(session=session, filter=filter)
    return returnessentia