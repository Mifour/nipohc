from pydantic import BaseModel


class QueryBase(BaseModel):
    input: str
    result: int | float | None = None

    class Config:
        orm_mode = True
