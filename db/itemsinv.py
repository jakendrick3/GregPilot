from sqlmodel import SQLModel, Field, Column, TIMESTAMP, text, Session, select, func
from datetime import datetime, timedelta, timezone
from .itemslog import ItemsLog
from .items import Items
from .craftables import Craftable
from pydantic import BaseModel
from .paginate import Paginate
from typing import Optional

class ItemsInvFilter(BaseModel):
    name: Optional[str] = None
    craftable: Optional[bool] = None

class ItemsInv(SQLModel):
    name: str
    size: int
    craftable: bool
    id: str
    ts: datetime


async def read_items_inv(*, session: Session, filter: ItemsInvFilter):
    cutoff = datetime.now(tz=timezone.utc) - timedelta(minutes=20)

    ranked = (
        select(
            ItemsLog,
            func.row_number()
            .over(
                partition_by=ItemsLog.id,
                order_by=ItemsLog.ts.desc()
            )
            .label("rnk")
        )
    ).subquery()

    main = (
        select(
            Items.name,
            ranked.c.size,
            Craftable.craftable,
            Items.id,
            ranked.c.ts
        )
        .join(ranked, ranked.c.id == Items.id)
        .join(Craftable, Craftable.itemid == Items.id, isouter=True)
        .where(ranked.c.rnk == 1)
        .where(ranked.c.ts > cutoff)
        .where(Items.name.not_like("%Coin%"))
    )

    if filter.name is not None:
        main = main.where(Items.name.contains(filter.name))
    
    if filter.craftable is not None:
        main = main.where(Craftable.craftable == filter.craftable)

    itemsq = session.exec(main).all()
    
    dictitems = [dict(item._mapping) for item in itemsq]

    returnitems = []
    for item in dictitems:
        if item["craftable"] is None:
            item["craftable"] = False
        validateditem = ItemsInv.model_validate(item)
        returnitems.append(validateditem)
    
    return returnitems