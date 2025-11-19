from sqlmodel import Field, SQLModel, Column, TIMESTAMP, text, Session, select

class Fluids(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str

async def read_fluids(*, session: Session, offset: int = 0, limit: int = 10000):
    returnfluids = session.exec(select(Fluids).offset(offset).limit(limit)).all()
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