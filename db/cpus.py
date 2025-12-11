from sqlmodel import SQLModel, Field, Column, TIMESTAMP, text, Session, select, func, delete

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

async def read_cpus(*, session: Session, offset: int = 0, limit: int = 10000):
    returncpus = session.exec(select(CPU).offset(offset).limit(limit)).all()
    
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