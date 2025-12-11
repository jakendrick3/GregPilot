from sqlmodel import SQLModel, Field, Column, TIMESTAMP, text, Session, select
from datetime import datetime

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

async def read_essentia_log(*, session: Session, offset: int = 0, limit: int = 10000):
    essentia = session.exec(select(EssentiaLog).offset(offset).limit(limit)).all()
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