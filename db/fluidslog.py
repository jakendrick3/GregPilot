from sqlmodel import SQLModel, Field, Column, TIMESTAMP, text, Session, select
from datetime import datetime
from pydantic import BaseModel
from .paginate import Paginate
from typing import Optional

class FluidsLogEntry(SQLModel):
    id: str = Field(foreign_key="fluids.id", nullable=False)
    amount: int

class FluidsLog(FluidsLogEntry, table=True):
    entryID: int | None = Field(default=None, primary_key=True)
    ts: datetime | None = Field(default=None, sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    ))

class FluidsLogFilter(BaseModel):
    id: Optional[str] = None
    newerthan: Optional[datetime] = None
    olderthan: Optional[datetime] = None

async def read_fluids_log(*, session: Session, paginate: Paginate, filter: FluidsLogFilter):
    query = select(FluidsLog).offset(paginate.offset).limit(paginate.limit)

    if filter.id is not None:
        query = query.where(FluidsLog.id == filter.id)

    if filter.newerthan is not None:
        query = query.where(FluidsLog.ts > filter.newerthan)

    if filter.olderthan is not None:
        query = query.where(FluidsLog.ts < filter.olderthan)

    items = session.exec(query).all()
    return items

async def create_fluids_log(*, session: Session, fluids: list[FluidsLogEntry]):
    fluidspublic = []
    for fluidentry in fluids:
        dbitem = FluidsLog.model_validate(fluidentry)
        session.add(dbitem)
        fluidspublic.append(dbitem)
    
    session.commit()
    for x in fluidspublic:
        session.refresh(x)

    return fluidspublic