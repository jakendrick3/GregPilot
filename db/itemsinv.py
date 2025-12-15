from sqlmodel import SQLModel, Field, Column, TIMESTAMP, text, Session, select, func
from datetime import datetime, timedelta, timezone
from .itemslog import ItemsLog
from .items import Items
from .craftables import Craftable

class ItemsInv(SQLModel):
    name: str
    size: int
    craftable: bool
    id: str
    ts: datetime


async def read_items_inv(*, session: Session):
    cutoff = datetime.now(tz=timezone.utc) - timedelta(minutes=20)

    sub = (
        select(
            ItemsLog.id.label("item_id"),
            func.max(ItemsLog.ts).label("latest_ts")
        )
        .group_by(ItemsLog.id)
    ).subquery()

    main = (
        select(
            Items.name,
            ItemsLog.size,
            Craftable.craftable,
            Items.id,
            ItemsLog.ts
        )
        .join(
            sub,
            (ItemsLog.id == sub.c.item_id) &
            (ItemsLog.ts == sub.c.latest_ts)
        )
        .join(Items, ItemsLog.id == Items.id, isouter=True)
        .join(Craftable, Craftable.itemid == Items.id, isouter=True)
        .where(ItemsLog.ts > cutoff)
        .where(Items.name.not_like("%Coin%"))
    )

    itemsq = session.exec(main).all()
    
    dictitems = [dict(item._mapping) for item in itemsq]

    returnitems = []
    for item in dictitems:
        if item["craftable"] is None:
            item["craftable"] = False
        validateditem = ItemsInv.model_validate(item)
        returnitems.append(validateditem)
    
    return returnitems