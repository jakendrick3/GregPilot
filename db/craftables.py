from sqlmodel import SQLModel, Field, Column, TIMESTAMP, text, Session, select, func, delete, or_
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel
from typing import Optional
from .paginate import Paginate

class CraftablePublic(SQLModel):
    craftable: bool = True
    type: str
    itemid: str | None = Field(foreign_key="items.id", default=None)
    fluidid: str | None = Field(foreign_key="fluids.id", default=None)
    

class Craftable(CraftablePublic, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ts: datetime | None = Field(default=None, sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    ))

class CraftableFilter(BaseModel):
    type: Optional[str] = None
    itemid: Optional[str] = None
    fluidid: Optional[str] = None

async def read_craftables(*, session: Session, paginate: Paginate, filter: CraftableFilter):
    query = select(Craftable).offset(paginate.offset).limit(paginate.limit)

    if filter.type is not None:
        query = query.where(Craftable.type == filter.type)
    
    if filter.itemid is not None:
        query = query.where(Craftable.itemid == filter.itemid)
    
    if filter.fluidid is not None:
        query = query.where(Craftable.fluidid == filter.fluidid)

    returncrafts = session.exec(query).all()    
    return returncrafts

async def create_craftables(*, session: Session, crafts: list[CraftablePublic]):
    cutoff = datetime.now(tz=timezone.utc) - timedelta(minutes=20)
    rmquery = delete(Craftable).where(Craftable.ts < cutoff)
    result = session.exec(rmquery)
    
    craftspublic = []
    for craft in crafts:
        if craft.type == "item":
            curritem = session.exec(select(Craftable).where(Craftable.itemid == craft.itemid))
            if curritem.first() is None:
                dbitem = Craftable.model_validate(craft)
                session.add(dbitem)
                craftspublic.append(dbitem)
        elif craft.type == "fluid":
            curritem = session.exec(select(Craftable).where(Craftable.fluidid == craft.fluidid))
            if curritem.first() is None:
                dbitem = Craftable.model_validate(craft)
                session.add(dbitem)
                craftspublic.append(dbitem)
    
    session.commit()
    for x in craftspublic:
        session.refresh(x)
    
    return craftspublic