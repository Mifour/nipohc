from sqlalchemy import BigInteger, Float, String, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Mapped, Session, mapped_column

from ..internal.algo import eval_RPN
from .db import Base


class Query(Base):
    __tablename__ = "query"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    input: Mapped[str] = mapped_column(String, unique=True, index=True)
    result: Mapped[float] = mapped_column(Float)

    def __repr__(self):
        return f"Query('{self.input}' = {self.result})"

    def to_dict(self):
        return {"input": self.input, "result": self.result}

    @classmethod
    def eval_and_insert(cls, input_str: str, session: Session):
        result = eval_RPN(input_str)
        stmt = insert(cls).values(input=input_str, result=result)

        # math operation are unique on their input and the result is always the same
        stmt = stmt.on_conflict_do_nothing(index_elements=[cls.input]).returning(cls)

        orm_stmt = select(cls).from_statement(stmt)
        if row := session.execute(orm_stmt).first():
            # created in the DB
            obj = row[0]
        else:
            # already exists in DB
            obj = cls(input=input_str, result=result)
        session.commit()
        return obj
