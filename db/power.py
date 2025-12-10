from sqlmodel import SQLModel, Field, Column, TIMESTAMP, text, Session, select, func, desc
from datetime import datetime, timedelta, timezone
from .powerlog import PowerLog

class Power(SQLModel):
    outputavg: int
    inputavg: int
    powerstored: int
    powermax: int
    ts: datetime


async def read_power(*, session: Session):
    cutoff = datetime.now(tz=timezone.utc) - timedelta(minutes=2)

    query = select(PowerLog).order_by(desc(PowerLog.ts)).limit(1)
    powerq = session.exec(query).first()
    
    validatedpower = Power.model_validate(powerq)
    
    return validatedpower