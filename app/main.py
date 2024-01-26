from fastapi import Depends, FastAPI

from .routers import rpn

app = FastAPI()


app.include_router(rpn.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Reverse Polish Notation calculator!"}
