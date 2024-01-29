from fastapi import FastAPI

from .routers import queries

app = FastAPI()


app.include_router(queries.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Reverse Polish Notation calculator!"}
