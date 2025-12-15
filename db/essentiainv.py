from sqlmodel import SQLModel, Field, Column, TIMESTAMP, text, Session, select, func
from datetime import datetime, timedelta, timezone
from .essentialog import EssentiaLog
from .essentia import Essentia

class EssentiaInv(SQLModel):
    name: str
    amount: int
    id: str
    ts: datetime


async def read_essentia_inv(*, session: Session):
    cutoff = datetime.now(tz=timezone.utc) - timedelta(minutes=20)

    sub = (
        select(
            EssentiaLog.id.label("essentia_id"),
            func.max(EssentiaLog.ts).label("latest_ts")
        )
        .group_by(EssentiaLog.id)
    ).subquery()

    main = (
        select(
            Essentia.name,
            EssentiaLog.amount,
            Essentia.id,
            EssentiaLog.ts
        )
        .join(
            sub,
            (EssentiaLog.id == sub.c.essentia_id) &
            (EssentiaLog.ts == sub.c.latest_ts)
        )
        .join(Essentia, EssentiaLog.id == Essentia.id, isouter=True)
        .where(EssentiaLog.ts > cutoff)
    )

    fluidsq = session.exec(main).all()
    
    dictitems = [dict(item._mapping) for item in fluidsq]

    returnfluids = []
    for item in dictitems:
        validateditem = EssentiaInv.model_validate(item)
        returnfluids.append(validateditem)
    
    return returnfluids