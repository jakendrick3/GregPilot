from sqlmodel import Field, SQLModel, Column, TIMESTAMP, text, Session, select
from datetime import datetime

class CraftRequestPublic(SQLModel):
    type: str
    id: str
    amount: int
    status: str | None = Field(default="pending")

class CraftRequest(CraftRequestPublic, table=True):
    requestid: int | None = Field(default=None, primary_key=True)
    entered: datetime | None = Field(default=None, sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    ))

async def read_craftrequests(*, session: Session, offset: int = 0, limit: int = 10000, all: bool = False):
    if all == True:
        returncrafts = session.exec(select(CraftRequest).offset(offset).limit(limit)).all()
    else:
        returncrafts = session.exec(select(CraftRequest).where(CraftRequest.status == "pending").offset(offset).limit(limit)).all()
    return returncrafts

async def create_craftrequests(*, session: Session, crafts: list[CraftRequestPublic]):
    craftreturn = []
    for craft in crafts:
        dbitem = CraftRequest.model_validate(craft)
        session.add(dbitem)
        craftreturn.append(dbitem)
    
    session.commit()
    for x in craftreturn:
        session.refresh(x)

    return craftreturn

async def update_craftrequests(*, session: Session, crafts: list[CraftRequest]):
    for request in crafts:
        session.add(request)
        
    session.commit()

    for request in crafts:
        session.refresh(request)
    
    return crafts