from pydantic import BaseModel

class Paginate(BaseModel):
    limit: int = 100
    offset: int = 0