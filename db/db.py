import os
import dotenv
from sqlmodel import SQLModel, create_engine, Session
from . import items, itemslog, fluids, fluidslog, power, essentia, essentialog, essentiainv

dotenv.load_dotenv(override=False)
dburl = os.getenv("GPDBURL")

engine = create_engine(dburl)

def create_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session