from fastapi import FastAPI
from .db import db
from .api import items_router, fluids_router

app = FastAPI()

app.include_router(items_router.router)
app.include_router(fluids_router.router)

db.create_db()