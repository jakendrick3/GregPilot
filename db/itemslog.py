from sqlmodel import SQLModel, Field, Column, TIMESTAMP, text, Session, select
from datetime import datetime
from pydantic import BaseModel
from .paginate import Paginate
from typing import Optional

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

class ItemsLogFilter(BaseModel):
    id: Optional[str] = None
    newerthan: Optional[datetime] = None
    olderthan: Optional[datetime] = None


async def read_items_log(*, session: Session, paginate: Paginate, filter: ItemsLogFilter):
    query = select(ItemsLog).offset(paginate.offset).limit(paginate.limit)

    if filter.id is not None:
        query = query.where(ItemsLog.id == filter.id)

    if filter.newerthan is not None:
        query = query.where(ItemsLog.ts > filter.newerthan)

    if filter.olderthan is not None:
        query = query.where(ItemsLog.ts < filter.olderthan)

    items = session.exec(query).all()
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

