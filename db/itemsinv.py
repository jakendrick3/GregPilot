from sqlmodel import SQLModel, Field, Column, TIMESTAMP, text, Session, select, func
from datetime import datetime, timedelta, timezone
from .itemslog import ItemsLog
from .items import Items

class ItemsInv(SQLModel):
    name: str
    size: int
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
        select(ItemsLog, Items)
        .join(
            sub,
            (ItemsLog.id == sub.c.item_id) &
            (ItemsLog.ts == sub.c.latest_ts)
        )
        .join(Items, ItemsLog.id == Items.id, isouter=True)
        .where(ItemsLog.ts > cutoff)
        .where(Items.name.not_like("%Coin%"))
    )

    itemsq = session.exec(main)
    
    returnitems = []
    for log, items in itemsq:
        combined = {
            'name': items.name,
            'size': log.size,
            'ts': log.ts
        }

        validateditem = ItemsInv.model_validate(combined)
        returnitems.append(validateditem)
    
    return returnitems