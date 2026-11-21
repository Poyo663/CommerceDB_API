from fastapi import FastAPI

from .routers import ComercioRouter, ProdutoRouter

app = FastAPI()

app.include_router(ComercioRouter.router, prefix="/comercio")
app.include_router(ProdutoRouter.router, prefix="/produto")

@app.get('/')
def hello_world():
    return "hello world"
