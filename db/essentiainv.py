from sqlmodel import SQLModel, Field, Column, TIMESTAMP, text, Session, select, func
from datetime import datetime, timedelta, timezone
from .essentialog import EssentiaLog
from .essentia import Essentia
from pydantic import BaseModel
from .paginate import Paginate
from typing import Optional

class EssentiaInvFilter(BaseModel):
    name: Optional[str] = None

class EssentiaInv(SQLModel):
    name: str
    amount: int
    id: str
    ts: datetime


async def read_essentia_inv(*, session: Session, filter: EssentiaInvFilter):
    cutoff = datetime.now(tz=timezone.utc) - timedelta(minutes=20)

    ranked_essentia = (
        select(
            EssentiaLog.id.label("essentia_id"),
            EssentiaLog.amount,
            EssentiaLog.ts,
            func.row_number()
            .over(
                partition_by=EssentiaLog.id,
                order_by=EssentiaLog.ts.desc()
            )
            .label("rnk")
        )
    ).subquery()

    main = (
        select(
            Essentia.name,
            ranked_essentia.c.amount,
            Essentia.id,
            ranked_essentia.c.ts
        )
        .join(ranked_essentia, ranked_essentia.c.essentia_id == Essentia.id)
        .where(ranked_essentia.c.rnk == 1)
        .where(ranked_essentia.c.ts > cutoff)
    )

    if filter.name is not None:
        main = main.where(Essentia.name.contains(filter.name))

    essentiaq = session.exec(main).all()
    
    dictitems = [dict(item._mapping) for item in essentiaq]

    returnfluids = []
    for item in dictitems:
        validateditem = EssentiaInv.model_validate(item)
        returnfluids.append(validateditem)
    
    return returnfluids