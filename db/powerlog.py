from sqlmodel import SQLModel, Field, Column, TIMESTAMP, text, Session, select
from datetime import datetime
from . import items

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


async def read_power_log(*, session: Session, offset: int = 0, limit: int = 10000):
    powerlogs = session.exec(select(PowerLog).offset(offset).limit(limit)).all()
    return powerlogs

async def create_power_log(*, session: Session, entry: PowerLogEntry):
    dbitem = PowerLog.model_validate(entry)
    
    session.add(dbitem)
    session.commit()
    session.refresh(dbitem)

    return dbitem