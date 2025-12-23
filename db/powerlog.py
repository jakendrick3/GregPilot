from sqlmodel import SQLModel, Field, Column, TIMESTAMP, text, Session, select
from datetime import datetime
from pydantic import BaseModel
from .paginate import Paginate
from typing import Optional

class PowerLogEntry(SQLModel):
    outputavg: int
    inputavg: int
    powerstored: int
    powermax: int

class PowerLog(PowerLogEntry, table=True):
    entryID: int | None = Field(default=None, primary_key=True)
    ts: datetime | None = Field(default=None, sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    ))

class PowerFilter(BaseModel):
    newerthan: Optional[datetime] = None
    olderthan: Optional[datetime] = None


async def read_power_log(*, session: Session, paginate: Paginate, filter: PowerFilter):
    query = select(PowerLog).offset(paginate.offset).limit(paginate.limit)

    if filter.newerthan is not None:
        query = query.where(PowerLog.ts > filter.newerthan)

    if filter.olderthan is not None:
        query = query.where(PowerLog.ts < filter.olderthan)

    powerlogs = session.exec(query).all()
    return powerlogs

async def create_power_log(*, session: Session, entry: PowerLogEntry):
    dbitem = PowerLog.model_validate(entry)
    
    session.add(dbitem)
    session.commit()
    session.refresh(dbitem)

    return dbitem