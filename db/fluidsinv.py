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

    ranked_fluids = (
        select(
            FluidsLog.id.label("fluid_id"),
            FluidsLog.amount,
            FluidsLog.ts,
            func.row_number()
            .over(
                partition_by=FluidsLog.id,
                order_by=FluidsLog.ts.desc()
            )
            .label("rnk")
        )
    ).subquery()

    main = (
        select(
            Fluids.name,
            ranked_fluids.c.amount,
            Craftable.c.craftable,
            Fluids.id,
            ranked_fluids.c.ts
        )
        .join(ranked_fluids, ranked_fluids.c.fluid_id == Fluids.id)
        .join(Craftable, Craftable.c.fluidid == Fluids.id, isouter=True)
        .where(ranked_fluids.c.rnk == 1)
        .where(ranked_fluids.c.ts > cutoff)
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