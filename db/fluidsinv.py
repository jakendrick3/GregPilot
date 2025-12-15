from sqlmodel import SQLModel, Field, Column, TIMESTAMP, text, Session, select, func
from datetime import datetime, timedelta, timezone
from .fluidslog import FluidsLog
from .fluids import Fluids
from .craftables import Craftable

class FluidsInv(SQLModel):
    name: str
    amount: int
    craftable: bool
    id: str
    ts: datetime


async def read_fluids_inv(*, session: Session):
    cutoff = datetime.now(tz=timezone.utc) - timedelta(minutes=20)

    sub = (
        select(
            FluidsLog.id.label("fluid_id"),
            func.max(FluidsLog.ts).label("latest_ts")
        )
        .group_by(FluidsLog.id)
    ).subquery()

    main = (
        select(
            Fluids.name,
            FluidsLog.amount,
            Craftable.craftable,
            Fluids.id,
            FluidsLog.ts
        )
        .join(
            sub,
            (FluidsLog.id == sub.c.fluid_id) &
            (FluidsLog.ts == sub.c.latest_ts)
        )
        .join(Fluids, FluidsLog.id == Fluids.id, isouter=True)
        .join(Craftable, Craftable.fluidid == Fluids.id, isouter=True)
        .where(FluidsLog.ts > cutoff)
    )

    fluidsq = session.exec(main).all()
    
    dictitems = [dict(item._mapping) for item in fluidsq]

    returnfluids = []
    for item in dictitems:
        if item["craftable"] is None:
            item["craftable"] = False
        validateditem = FluidsInv.model_validate(item)
        returnfluids.append(validateditem)
    
    return returnfluids