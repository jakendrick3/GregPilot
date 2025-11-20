from sqlmodel import SQLModel, Field, Column, TIMESTAMP, text, Session, select, func
from datetime import datetime, timedelta, timezone
from .fluidslog import FluidsLog
from .fluids import Fluids

class FluidsInv(SQLModel):
    name: str
    amount: int
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
        select(FluidsLog, Fluids)
        .join(
            sub,
            (FluidsLog.id == sub.c.fluid_id) &
            (FluidsLog.ts == sub.c.latest_ts)
        )
        .join(Fluids, FluidsLog.id == Fluids.id, isouter=True)
        .where(FluidsLog.ts > cutoff)
    )

    fluidsq = session.exec(main)
    
    returnfluids = []
    for log, fluids in fluidsq:
        combined = {
            'name': fluids.name,
            'amount': log.amount,
            'ts': log.ts
        }

        validateditem = FluidsInv.model_validate(combined)
        returnfluids.append(validateditem)
    
    return returnfluids