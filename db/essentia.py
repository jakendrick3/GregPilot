from sqlmodel import Field, SQLModel, Column, TIMESTAMP, text, Session, select
from pydantic import BaseModel
from typing import Optional
from .paginate import Paginate

class Essentia(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str

class EssentiaFilter(BaseModel):
    name: Optional[str] = None

async def read_essentia(*, session: Session, paginate: Paginate, filter: EssentiaFilter):
    query = select(Essentia).offset(paginate.offset).limit(paginate.limit)

    if filter.name is not None:
        query = query.where(Essentia.name.contains(filter.name))
    
    returness = session.exec(query).all()
    return returness

async def create_essentia(*, session: Session, essentia: list[Essentia]):
    essentiareturn = []
    for essense in essentia:
        curritem = session.exec(select(Essentia).where(Essentia.id == essense.id))
        if curritem.first() is None:            
            dbitem = Essentia.model_validate(essense)
            session.add(dbitem)
            essentiareturn.append(dbitem)
    
    session.commit()
    for x in essentiareturn:
        session.refresh(x)

    return essentiareturn