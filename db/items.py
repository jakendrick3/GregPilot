from sqlmodel import Field, SQLModel, Column, TIMESTAMP, text, Session, select
from pydantic import BaseModel
from typing import Optional
from .paginate import Paginate

class ItemsFilter(BaseModel):
    name: Optional[str] = None

class Items(SQLModel, table=True):
    id: str = Field(primary_key=True)
    rawid: str | None = None
    rawdamage: str | None = None
    name: str


async def read_items(*, session: Session, paginate: Paginate, filter: ItemsFilter):
    query = select(Items).offset(paginate.offset).limit(paginate.limit)

    if filter.name is not None:
        query = query.where(Items.name.contains(filter.name))

    items = session.exec(query).all()
    return items

async def create_items(*, session: Session, items: list[Items]):
    itemspublic = []
    for itementry in items:
        curritem = session.exec(select(Items).where(Items.id == itementry.id))
        if curritem.first() is None:
            if not itementry.rawid or not itementry.rawdamage:
                blocks = itementry.id.split(":")
                itementry.rawid = blocks[0]
                itementry.rawdamage = blocks[1]
            
            dbitem = Items.model_validate(itementry)
            session.add(dbitem)
            itemspublic.append(dbitem)
    
    session.commit()
    for x in itemspublic:
        session.refresh(x)

    return itemspublic