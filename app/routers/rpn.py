import logging
from typing import Annotated

from fastapi import APIRouter, Query, Body, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from ..internal.algo import eval_RPN


router = APIRouter()

logger = logging.getLogger("RPN")



@router.get("/rpn")
async def get_rpn(input_str: Annotated[str , Query(min_length=5, max_length=50, example="1_3_%2B")]) -> int | float:
    # parse the query_args
    # special characters can be escaped like so: 
    # * is %2A
    # + is %2B
    # - is %2D
    # / is %2F
    # see more at https://www.w3schools.com/tags/ref_urlencode.asp
    try:
        return eval_RPN(input_str.replace("_", " "))
    except Exception as e:
        logger.error(f"ValueError: {e}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"detail": "Could not process value", "body": input_str}),
        )


@router.post("/rpn")
async def post_rpn(input_str: Annotated[str , Body(min_length=5, max_length=50, example="1 3 +")]) -> int | float:
    # parse the body
    try:
        return eval_RPN(input_str)
    except Exception as e:
        logger.error(f"ValueError: {e}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"detail": "Could not process value", "body": input_str}),
        )


@router.get("/export")
async def export():
    # export the previous queries as csv
    return None
