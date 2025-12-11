from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from ..db import db, essentia, essentialog, essentiainv

router = APIRouter(
    tags=["essentia"],
    responses={404: {"description": "Not found"}}
)

@router.get("/api/essentia", response_model=list[essentia.Essentia])
async def get_essentia(*, session: Session = Depends(db.get_session), offset: int = 0, limit: int = Query(default=10000, le=10000)):
    returnessentia = await essentia.read_essentia(session=session, offset=offset, limit=limit)
    return returnessentia

@router.post("/api/essentia", response_model=list[essentia.Essentia])
async def post_essentia(*, session: Session = Depends(db.get_session), postessentia: list[essentia.Essentia]):
    return await essentia.create_essentia(session=session, essentia=postessentia)

@router.get("/api/essentia/log", response_model=list[essentialog.EssentiaLog])
async def get_essentia_log(*, session: Session = Depends(db.get_session), offset: int = 0, limit: int = Query(default=10000, le=10000)):
    returnessentia = await essentialog.read_essentia_log(session=session, offset=offset, limit=limit)
    return returnessentia

@router.post("/api/essentia/log", response_model=list[essentialog.EssentiaLog])
async def post_essentia_log(*, session: Session = Depends(db.get_session), essentia: list[essentialog.EssentiaLog]):
    return await essentialog.create_essentia_log(session=session, essentia=essentia)

@router.get("/api/essentia/inv", response_model=list[essentiainv.EssentiaInv])
async def get_essentia_log(*, session: Session = Depends(db.get_session)):
    returnessentia = await essentiainv.read_essentia_inv(session=session)
    return returnessentia