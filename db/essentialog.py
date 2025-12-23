from sqlmodel import SQLModel, Field, Column, TIMESTAMP, text, Session, select
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from .paginate import Paginate

class EssentiaLogEntry(SQLModel):
    id: str = Field(foreign_key="essentia.id", nullable=False)
    amount: int

class EssentiaLog(EssentiaLogEntry, table=True):
    entryID: int | None = Field(default=None, primary_key=True)
    ts: datetime | None = Field(default=None, sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    ))

class EssentiaLogFilter(BaseModel):
    id: Optional[str] = None
    newerthan: Optional[datetime] = None
    olderthan: Optional[datetime] = None

async def read_essentia_log(*, session: Session, paginate: Paginate, filter: EssentiaLogFilter):
    query = select(EssentiaLog).offset(paginate.offset).limit(paginate.limit)

    if filter.id is not None:
        query = query.where(EssentiaLog.id == filter.id)

    if filter.newerthan is not None:
        query = query.where(EssentiaLog.ts > filter.newerthan)

    if filter.olderthan is not None:
        query = query.where(EssentiaLog.ts < filter.olderthan)
    
    essentia = session.exec(query).all()
    return essentia

async def create_essentia_log(*, session: Session, essentia: list[EssentiaLogEntry]):
    essentiareturn = []
    for essense in essentia:
        dbitem = EssentiaLog.model_validate(essense)
        session.add(dbitem)
        essentiareturn.append(dbitem)
    
    session.commit()
    for x in essentiareturn:
        session.refresh(x)

    return essentiareturn