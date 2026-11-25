from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import ComercioRouter, ProdutoRouter, UsuarioRouter

app = FastAPI()

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"]
)

app.include_router(ComercioRouter.router, prefix="/comercio")
app.include_router(ProdutoRouter.router, prefix="/produto")
app.include_router(UsuarioRouter.router, prefix="/usuario")

@app.get('/')
def hello_world():
    return "hello world"
