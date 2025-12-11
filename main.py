import sched
import time
import threading
from fastapi import FastAPI
from sqlmodel import Session
from contextlib import asynccontextmanager
from GregPilot.db import db, server
from GregPilot.api import items_router, fluids_router, oc_router, server_router, power_router, essentia_router

scheduler = sched.scheduler(time.time, time.sleep)

db.create_db()

def ScheduleQuery():
    with Session(db.engine) as session:
        server.QueryServer(session=session)

    scheduler.enter(10, 1, ScheduleQuery)

def start_scheduler():
    scheduler.enter(0, 1, ScheduleQuery)
    scheduler.run()

@asynccontextmanager
async def lifespan(app: FastAPI):
    t = threading.Thread(target=start_scheduler, daemon=True)
    t.start()
    yield

app = FastAPI(
    title="GregPilot Server",
    description="Controller for ME/AE2 system logging and orders",
    version="0.1.0",
    contact={
        "name": "Alex Kendrick",
        "email": "alex@alex-kendrick.com"
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0",
    },
    lifespan=lifespan
)

app.include_router(items_router.router)
app.include_router(fluids_router.router)
app.include_router(oc_router.router)
app.include_router(server_router.router)
app.include_router(power_router.router)
app.include_router(essentia_router.router)