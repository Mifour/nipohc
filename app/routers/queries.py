import logging
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, StreamingResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..sqla import models, schemas
from ..sqla.db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


router = APIRouter()

logger = logging.getLogger("Queries")


# Dependency
def get_session():
    session = SessionLocal()
    session.flush()
    try:
        yield session
    finally:
        session.close()


@router.get("/query/", response_model=schemas.QueryBase)
def get_query(
    input_str: Annotated[str, Query(min_length=5, max_length=50, example="1_3_%2B")],
    session: Session = Depends(get_session),
) -> schemas.QueryBase:
    # parse the query_args
    # special characters can be escaped like so:
    # * is %2A
    # + is %2B
    # - is %2D
    # / is %2F
    # see more at https://www.w3schools.com/tags/ref_urlencode.asp
    try:
        _input_str = input_str.replace("_", " ")
        obj = models.Query.eval_and_insert(_input_str, session)
        return schemas.QueryBase(input=obj.input, result=obj.result)
    except Exception as e:
        logger.exception(f"GET query/{input_str} : {e}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder(
                {"detail": "Could not process value", "body": input_str or None}
            ),
        )


@router.post("/query/", response_model=schemas.QueryBase)
def post_query(
    input_str: Annotated[str, Body(min_length=5, max_length=50, example="1_3_%2B")],
    session: Session = Depends(get_session),
) -> int | float:
    # parse the body
    try:
        obj = models.Query.eval_and_insert(input_str, session)
        return schemas.QueryBase(input=obj.input, result=obj.result)
    except Exception as e:
        logger.error(f"ValueError: {e}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder(
                {"detail": "Could not process value", "body": input_str}
            ),
        )


@router.get("/export/")
def export(session: Session = Depends(get_session)):
    def iter_table():
        # A proper streaming export from PG with an async driver would be better
        byte_content = b'input,result\n'
        for row in session.execute(select(models.Query)).scalars():
            byte_content +=  str(row.input).encode() + b',' + str(row.result).encode() + b'\n'
        yield from [byte_content]
    return StreamingResponse(iter_table(), media_type="application/csv")
