from sqlmodel import Field, SQLModel, Column, TIMESTAMP, text, Session, select

class Items(SQLModel, table=True):
    id: str = Field(primary_key=True)
    rawid: str | None = None
    rawdamage: int | None = None
    name: str


async def read_items(*, session: Session, offset: int = 0, limit: int = 10000):
    items = session.exec(select(Items).offset(offset).limit(limit)).all()
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