from fastapi import FastAPI

from .routers import ComercioRouter, ProdutoRouter, UsuarioRouter

app = FastAPI()

app.include_router(ComercioRouter.router, prefix="/comercio")
app.include_router(ProdutoRouter.router, prefix="/produto")
app.include_router(UsuarioRouter.router, prefix="/usuario")

@app.get('/')
def hello_world():
    return "hello world"
