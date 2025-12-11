from sqlmodel import Field, SQLModel, Column, TIMESTAMP, text, Session, select

class Essentia(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str

async def read_essentia(*, session: Session, offset: int = 0, limit: int = 10000):
    returness = session.exec(select(Essentia).offset(offset).limit(limit)).all()
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