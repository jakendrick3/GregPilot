from sqlmodel import SQLModel, Field, Column, TIMESTAMP, text, Session, select
from datetime import datetime
from . import items

class ItemsLogEntry(SQLModel):
    id: str = Field(foreign_key="items.id", nullable=False)
    size: int

class ItemsLog(ItemsLogEntry, table=True):
    entryID: int | None = Field(default=None, primary_key=True)
    ts: datetime | None = Field(default=None, sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    ))


async def read_items_log(*, session: Session, offset: int = 0, limit: int = 10000):
    items = session.exec(select(ItemsLog).offset(offset).limit(limit)).all()
    return items

async def create_items_log(*, session: Session, items: list[ItemsLogEntry]):
    itemspublic = []
    for itementry in items:
        dbitem = ItemsLog.model_validate(itementry)
        session.add(dbitem)
        itemspublic.append(dbitem)
    
    session.commit()
    for x in itemspublic:
        session.refresh(x)

    return itemspublic

