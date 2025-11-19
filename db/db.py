from sqlmodel import SQLModel, create_engine, Session
from . import items, itemslog, fluids, fluidslog

dburl = "postgresql://testgreg:test@postgres/testgreg"
engine = create_engine(dburl)

def create_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session