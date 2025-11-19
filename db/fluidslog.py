from sqlmodel import SQLModel, Field, Column, TIMESTAMP, text, Session, select
from datetime import datetime

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

async def read_fluids_log(*, session: Session, offset: int = 0, limit: int = 10000):
    items = session.exec(select(FluidsLog).offset(offset).limit(limit)).all()
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