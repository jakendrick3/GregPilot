from fastapi import FastAPI
from .db import db
from .api import items_router, fluids_router, oc_router


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
)

app.include_router(items_router.router)
app.include_router(fluids_router.router)
app.include_router(oc_router.router)

db.create_db()