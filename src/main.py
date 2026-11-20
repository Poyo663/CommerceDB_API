from fastapi import FastAPI

from .routers import ComercioRouter

app = FastAPI()

app.include_router(ComercioRouter.router, prefix="/comercio")

@app.get('/')
def hello_world():
    return "hello world"
