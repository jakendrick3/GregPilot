from sqlmodel import Field, SQLModel, Column, TIMESTAMP, text, Session, select
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from .paginate import Paginate

class CraftRequestPublic(SQLModel):
    type: str
    id: str
    amount: int
    status: str | None = Field(default="pending")

class CraftRequest(CraftRequestPublic, table=True):
    requestid: int | None = Field(default=None, primary_key=True)
    entered: datetime | None = Field(default=None, sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    ))

class CraftRequestFilter(BaseModel):
    type: Optional[str] = None
    id: Optional[str] = None
    status: Optional[str] = None
    newerthan: Optional[datetime] = None
    olderthan: Optional[datetime] = None

async def read_craftrequests(*, session: Session, paginate: Paginate, filter: CraftRequestFilter):
    query = select(CraftRequest).offset(paginate.offset).limit(paginate.limit)

    if filter.type is not None:
        query = query.where(CraftRequest.type == filter.type)
    
    if filter.id is not None:
        query = query.where(CraftRequest.id == filter.id)

    if filter.status is not None:
        query = query.where(CraftRequest.status == filter.status)

    if filter.newerthan is not None:
        query = query.where(CraftRequest.ts > filter.newerthan)

    if filter.olderthan is not None:
        query = query.where(CraftRequest.ts < filter.olderthan)

    returncrafts = session.exec(query).all()
    return returncrafts

async def create_craftrequests(*, session: Session, crafts: list[CraftRequestPublic]):
    craftreturn = []
    for craft in crafts:
        dbitem = CraftRequest.model_validate(craft)
        session.add(dbitem)
        craftreturn.append(dbitem)
    
    session.commit()
    for x in craftreturn:
        session.refresh(x)

    return craftreturn

async def update_craftrequests(*, session: Session, crafts: list[CraftRequest]):
    for request in crafts:
        session.add(request)
        
    session.commit()

    for request in crafts:
        session.refresh(request)
    
    return crafts