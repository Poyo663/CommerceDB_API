from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import Connection, text

from ..utils.db import connection_established

class Produto(BaseModel):
    id: int | None
    nome: str
    preco: float

class ProdutoRequestModel(BaseModel):
    api_key: str
    produtos: list[Produto]

class ProdutoTableModel():
    @staticmethod
    @connection_established
    def fetch_all(api_key: str, conn: Connection) -> list[Produto]:
        something = conn.execute(
                text(
                    """
                    SELECT p.id, p.nome_item, p.preco FROM
                    Comercio as c INNER JOIN Produto as p
                    ON c.id = p.id_comercio
                    WHERE c.apikey_crypt = :key
                    """
                    ), { "key": api_key }
        ).all()
        res = []
        for p in something:
            res.append(Produto(id=p[0], nome=p[1], preco=p[2]))
        return res

    def __init__(self, produto: ProdutoRequestModel) -> None:
        self.api_key = produto.api_key
        self.produtos = produto.produtos

    @connection_established
    def build(self, conn: Connection) -> list[Produto]:
        rows = conn.execute(
                text(
                    "SELECT id FROM Comercio WHERE apikey_crypt = :key"
                    ), { "key": self.api_key }
        ).all()
        if len(rows) < 1:
            raise HTTPException(status_code=404, detail="Could not find your comercio")
        commerceId = rows[0][0]

        prodObjs = []
        for prod in self.produtos:
            prodObjs.append({
                "id_comercio": commerceId,
                "nome_item": prod.nome,
                "preco": prod.preco
            })

        conn.execute(
                text(
                    "INSERT INTO Produto(id_comercio, nome_item, preco) VALUES (:id_comercio, :nome_item, :preco)"
                    ), prodObjs
        )
        conn.commit()
        print(self.produtos)
        return self.produtos
