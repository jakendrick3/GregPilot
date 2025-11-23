import os
import dotenv
from mcstatus import JavaServer
from sqlmodel import SQLModel, Field, Session, TIMESTAMP, Column, text, select, desc
from datetime import datetime

dotenv.load_dotenv(override=False)
serverurl = os.getenv("GPSERVERURL")

class ServerLog(SQLModel, table=True):
    entryID: int | None = Field(default=None, primary_key=True)
    online: bool
    players: str = Field(default='')
    ts: datetime | None = Field(default=None, sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    ))

class ServerStatus(SQLModel):
    online: bool
    players: list


def QueryServer(*, session: Session):
    try:
        server = JavaServer(serverurl)
        server.ping()
        ping = True
    except:
        ping = False

    if ping:
        query = server.query()

        data = {
            'online': True,
        }

        if len(query.players.names) == 1:
            data['players'] = query.players.names[0]
        elif len(query.players.names) == 0:
            data['players'] = ''
        else:
            data['players'] = ','.join(query.players.names)
        
        entry = ServerLog.model_validate(data)
        session.add(entry)
        session.commit()
    else:
        data = {
            'online': False
        }

        entry = ServerLog.model_validate(data)
        session.add(entry)
        session.commit()

async def read_server_status(*, session: Session):
    statusq = select(ServerLog).order_by(desc(ServerLog.ts))
    statusraw = session.exec(statusq).first()

    status = {
        'online': statusraw.online,
        'players': statusraw.players.split(',')
    }

    returnstatus = ServerStatus.model_validate(status)

    return returnstatus