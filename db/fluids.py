from sqlmodel import Field, SQLModel, Column, TIMESTAMP, text, Session, select
from pydantic import BaseModel
from typing import Optional
from .paginate import Paginate

class Fluids(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str

class FluidsFilter(BaseModel):
    name: Optional[str] = None

async def read_fluids(*, session: Session, paginate: Paginate, filter: FluidsFilter):
    query = select(Fluids).offset(paginate.offset).limit(paginate.limit)

    if filter.name is not None:
        query = query.where(Fluids.name.contains(filter.name))

    returnfluids = session.exec(query).all()
    return returnfluids

async def create_fluids(*, session: Session, fluids: list[Fluids]):
    fluidspublic = []
    for fluidentry in fluids:
        curritem = session.exec(select(Fluids).where(Fluids.id == fluidentry.id))
        if curritem.first() is None:            
            dbitem = Fluids.model_validate(fluidentry)
            session.add(dbitem)
            fluidspublic.append(dbitem)
    
    session.commit()
    for x in fluidspublic:
        session.refresh(x)

    return fluidspublic