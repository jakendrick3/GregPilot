from fastapi import APIRouter, Depends
from sqlmodel import Session
from ..db import db, server

router = APIRouter(
    tags=["server"],
    responses={404: {"description": "Not found"}}
)

@router.get("/server", response_model=server.ServerStatus)
async def get_items(*, session: Session = Depends(db.get_session)):
    status = await server.read_server_status(session=session)
    return status