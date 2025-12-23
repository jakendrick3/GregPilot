from sqlmodel import SQLModel, Field, Column, TIMESTAMP, text, Session, select, func, delete
from pydantic import BaseModel
from typing import Optional
from .paginate import Paginate

class CPUPublic(SQLModel):
    id: int | None = None
    name: str
    storage: int
    coprocessors: int
    busy: bool
    pendingitems: str
    activeitems: str

class CPU(CPUPublic, table=True):
    key: int | None = Field(default=None, primary_key=True)

class CPUFilter(BaseModel):
    name: Optional[str] = None
    busy: Optional[bool] = None

async def read_cpus(*, session: Session, paginate: Paginate, filter: CPUFilter):
    query = select(CPU).offset(paginate.offset).limit(paginate.limit)
    
    if filter.name is not None:
        query = query.where(CPU.name.contains(filter.name))
    
    if filter.busy is not None:
        query = query.where(CPU.busy == filter.busy)
    
    returncpus = session.exec(query).all()
    return returncpus

async def create_cpus(*, session: Session, cpus: list[CPUPublic]):
    rmquery = delete(CPU)
    result = session.exec(rmquery)
    
    cpuspublic = []
    nextid = 1
    for cpu in cpus:
        cpu.id = nextid
        nextid = nextid + 1

        dbitem = CPU.model_validate(cpu)
        session.add(dbitem)
        cpuspublic.append(dbitem)
    
    session.commit()
    for x in cpuspublic:
        session.refresh(x)
    
    return cpuspublic