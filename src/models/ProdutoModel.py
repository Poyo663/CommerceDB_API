from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sqlalchemy import Connection, text

from ..utils.db import connection_established
from ..utils.hash import hash

class Produto(BaseModel):
    nome: str = Field(
            ...,
            min_length=2,
            max_length=255,
            description='Nome do produto',
            examples=['Pastel de frango com catupiry', 'Parafuso pequeno']
        )
    preco: float = Field(
            ...,
            gt=0,
            description='Preço do produto',
            examples=[9.99, 5]
        )

class ProdutoRequestModel(BaseModel):
    api_key: str = Field(
            ...,
            min_length=10,
            max_length=255,
            description='Chave de API fornecida pela API',
            examples=['inv_admin_dLLvsZHFILBQ3IoD23_Y5R1nQZ41LEI9f-bvVBdJtf0']
        )
    produtos: list[Produto] = Field(
            ...,
            min_length=0,
            description='Lista de produtos a se adicionar',
            examples=[[{ 'nome': 'Pastel de frango com catupiry', 'preco': 9.99 }, { 'nome': 'Parafuso pequeno', 'preco': 5}]]
        )

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
                    ), { "key": hash(api_key) }
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
                    ), { "key": hash(self.api_key) }
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
        return self.produtos
